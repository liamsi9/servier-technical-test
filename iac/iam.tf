data "google_storage_project_service_account" "gcs_account" {
  project  = var.project
}

resource "google_service_account" "account" {
  account_id   = "gcf-sa"
  display_name = "GCF Service Account"
  project  = var.project

}
resource "google_pubsub_topic_iam_binding" "binding" {
  topic   = google_pubsub_topic.bqjobcompleted.id
  role    = "roles/pubsub.publisher"
  members = ["serviceAccount:${data.google_storage_project_service_account.gcs_account.email_address}"]
}

resource "google_project_iam_member" "permissions" {
  for_each = toset([
    "bigquery.dataEditor",
    "bigquery.jobUser",
    "datastore.viewer",
    "storage.admin"
  ])
  provider = google-beta
  project  = var.project
  role     = "roles/${each.key}"
  member   = "serviceAccount:${google_service_account.account.email}"
}