# Hugging Face Dataset Persistence
import os, json
from huggingface_hub import HfApi, HfFileSystem

class HFDatasetMemory:
    def __init__(self, repo_id: str = None, file_path: str = "data/memory.json"):
        self.repo_id = repo_id or os.getenv("HF_DATASET_REPO")
        self.file_path = file_path
        self.token = os.getenv("HF_TOKEN")
        self.api = HfApi(token=self.token)
        self.fs = HfFileSystem(token=self.token)
        if not self.repo_id:
            print("⚠️ HF_DATASET_REPO not set — using local file only.")

    def save(self, data: dict):
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        json.dump(data, open(self.file_path, "w"), indent=2)
        if not self.repo_id or not self.token:
            return "Saved locally (no HF repo configured)."
        print(f"📤 Uploading memory.json to {self.repo_id} ...")
        with open(self.file_path, "rb") as f:
            self.api.upload_file(
                path_or_fileobj=f,
                path_in_repo="memory.json",
                repo_id=self.repo_id,
                repo_type="dataset",
            )
        return "Uploaded memory.json to Hugging Face Dataset."

    def load(self):
        if self.repo_id and self.token:
            try:
                print(f"📥 Loading memory.json from {self.repo_id} ...")
                with self.fs.open(f"datasets/{self.repo_id}/memory.json") as f:
                    data = json.load(f)
                    json.dump(data, open(self.file_path, "w"), indent=2)
                    return data
            except Exception as e:
                print(f"⚠️ Remote load failed: {e}")
        if os.path.exists(self.file_path):
            return json.load(open(self.file_path))
        print("⚠️ No existing memory found.")
        return []
