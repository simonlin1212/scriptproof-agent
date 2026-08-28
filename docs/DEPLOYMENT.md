# Cloud Run deployment runbook

This runbook reflects the production deployment completed on 2026-08-28.

## Services and identity

- Cloud Run service: `scriptproof-web`
- Service account: `scriptproof-runtime`
- Vertex AI location: `global`
- Cloud Run region: `asia-southeast1`
- Secrets: `scriptproof-parallel-key`, `scriptproof-reviewer-code`
- Live service: `https://scriptproof-web-388088752401.asia-southeast1.run.app/`

The runtime identity needs only:

- `roles/aiplatform.user`
- `roles/secretmanager.secretAccessor` on the two ScriptProof secrets

## Build and deploy

```bash
export PATH="/opt/homebrew/share/google-cloud-sdk/bin:$PATH"
export PROJECT_ID="your-project-id"
export REGION="asia-southeast1"

gcloud run deploy scriptproof-web \
  --source=. \
  --project="$PROJECT_ID" \
  --region="$REGION" \
  --service-account="scriptproof-runtime@${PROJECT_ID}.iam.gserviceaccount.com" \
  --allow-unauthenticated \
  --timeout=600 \
  --memory=1Gi \
  --cpu=1 \
  --max-instances=1 \
  --set-env-vars="GOOGLE_CLOUD_PROJECT=${PROJECT_ID},GOOGLE_CLOUD_LOCATION=global,GOOGLE_GENAI_USE_VERTEXAI=TRUE,SCRIPT_PROOF_MODEL=gemini-3.5-flash" \
  --set-secrets="PARALLEL_API_KEY=scriptproof-parallel-key:latest,SCRIPT_PROOF_ACCESS_CODE=scriptproof-reviewer-code:latest"
```

## Credential rotation

Cloud Run resolves environment-variable secrets when an instance starts. A safe
rotation must not leave the production revision on `latest`, because a newly
started instance could receive an unvalidated secret version.

1. Before adding the new secret version, roll production to an explicit pin of
   the currently verified Secret Manager version.
2. Create the replacement Parallel credential and add it as a new Secret Manager
   version without changing production traffic.
3. Create a tagged `--no-traffic` Cloud Run candidate pinned to that exact new
   secret version. Do not use `latest` for either revision during rotation.
4. Run the health, access-control, and live research checks against the tagged
   candidate URL.
5. Shift traffic to the verified candidate, confirm the public service again,
   and only then revoke the old Parallel credential and disable its old secret
   version.

If the candidate fails, leave production traffic on the old pinned revision and
discard the candidate. This preserves a working rollback path throughout the
rotation.

## Verification

1. `GET /health` returns `{"service":"scriptproof","status":"ok"}`. **Passed.**
2. A missing reviewer code returns HTTP 403 without starting a provider call. **Passed.**
3. The sample screenplay completes end to end. **Passed.**
4. The report includes at least one Parallel-backed source and a non-zero Parallel tool-call count. **Passed: six calls and six preserved sources.**
5. Browser QA covers desktop and mobile-width layouts. **Passed: 16 assertions and visual inspection.**
6. Cloud Logging contains no screenplay text or active credential values. **Passed after log-safety hardening.**
