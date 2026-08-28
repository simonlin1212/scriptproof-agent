# Cloud Run deployment runbook

This runbook is intentionally not executed until the live Parallel smoke test passes.

## Services and identity

- Cloud Run service: `scriptproof-web`
- Service account: `scriptproof-runtime`
- Vertex AI location: `global`
- Cloud Run region: `asia-southeast1`
- Secrets: `scriptproof-parallel-key`, `scriptproof-reviewer-code`

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

## Verification

1. `GET /health` returns `{"service":"scriptproof","status":"ok"}`.
2. A missing reviewer code returns HTTP 403 without starting a provider call.
3. The sample screenplay completes end to end.
4. The report includes at least one Parallel-backed source and a non-zero Parallel tool-call count.
5. Browser QA covers desktop and mobile-width layouts.
6. Cloud Logging contains no screenplay text or credential values.
