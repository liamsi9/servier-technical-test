
resource "google_storage_bucket" "configurations" {
  provider                    = google-beta
  project                     = var.project
  name                        = "servier-technical-test"
  location                    = "EU"
  force_destroy               = true
  uniform_bucket_level_access = false
  public_access_prevention    = "enforced"
}

resource "google_storage_bucket" "bucket" {
  name     = "01-data-extraction"
  location = "EU"
  project  = var.project

}

resource "google_storage_bucket" "terraformdeploy" {
  name     = "gcs-terraform-deploy"
  location = "EU"
  project  = var.project

}

resource "google_storage_bucket_object" "object" {
  name   = "index.zip"
  bucket = google_storage_bucket.terraformdeploy.name
  source = "./modules/data_extraction.zip"

}
