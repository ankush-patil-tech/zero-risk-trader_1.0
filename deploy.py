import subprocess
import sys
import time
from datetime import timedelta


def run(cmd, title=None, allow_block=False):
    if title:
        print(f"\n🔹 {title}")

    print(f">>> RUNNING: {cmd}")
    start = time.time()

    # log tail should block, others should not
    result = subprocess.run(cmd, shell=True) if not allow_block else subprocess.call(cmd, shell=True)

    elapsed = time.time() - start
    elapsed_str = str(timedelta(seconds=int(elapsed)))

    if not allow_block and result.returncode != 0:
        print(f"\n❌ FAILED after {elapsed_str}")
        print(f"❌ Command: {cmd}")
        sys.exit(result.returncode)

    if not allow_block:
        print(f"✅ DONE in {elapsed_str}")


overall_start = time.time()

print("\n🚀 Starting full Docker + Azure deployment pipeline...\n")

# --- LOCAL CLEANUP ---
run("docker-compose down", "Stopping existing containers")
run("docker system prune -af", "Cleaning unused Docker resources")
run("docker builder prune -af", "Cleaning Docker build cache")

# --- LOCAL BUILD & RUN ---
run("docker-compose build", "Building docker-compose services")
run("docker-compose up -d", "Starting docker-compose services")
run("docker-compose ps", "Checking running containers")

# --- DOCKER HUB ---
run(
    "docker build --no-cache -t ankushp1650/zerorisktrader-python-app:v3 .",
    "Building Docker image for Docker Hub"
)
run(
    "docker push ankushp1650/zerorisktrader-python-app:v3",
    "Pushing image to Docker Hub"
)

# --- AZURE LOGIN ---
run("az login", "Logging into Azure")
run(
    "az acr login --name zerorisktradercontaner",
    "Logging into Azure Container Registry (ACR)"
)

# --- AZURE ACR BUILD & PUSH ---
run(
    "docker build --no-cache -t zerorisktradercontaner.azurecr.io/zerorisktrader-python-app:v3 .",
    "Building Docker image for Azure ACR"
)
# --- AZURE LOGIN ---
run("az login", "Logging into Azure")
run(
    "az acr login --name zerorisktradercontaner",
    "Logging into Azure Container Registry (ACR)"
)

run(
    "docker push zerorisktradercontaner.azurecr.io/zerorisktrader-python-app:v3",
    "Pushing image to Azure ACR"
)

# --- ENABLE AZURE DOCKER LOGGING ---
run(
    "az webapp log config --name ZeroRiskTrader --resource-group ZeroRiskTrader-RG-NM --docker-container-logging filesystem",
    "Enabling Azure Docker container logging"
)

# --- RESTART AZURE WEB APP ---
run(
    "az webapp restart --name ZeroRiskTrader --resource-group ZeroRiskTrader-RG-NM",
    "Restarting Azure Web App (ZeroRiskTrader)"
)

# --- FINAL SUMMARY ---
overall_elapsed = time.time() - overall_start
overall_elapsed_str = str(timedelta(seconds=int(overall_elapsed)))

print("\n🎉 DEPLOYMENT PIPELINE COMPLETED SUCCESSFULLY")
print(f"⏱️ Total time taken: {overall_elapsed_str}")
print("📡 Starting live Azure log stream...\n")

# --- LIVE LOG TAIL (BLOCKING ON PURPOSE) ---
run(
    "az webapp log tail --name ZeroRiskTrader --resource-group ZeroRiskTrader-RG-NM",
    title="Live Azure Logs (CTRL + C to stop)",
    allow_block=True
)
