resource "google_pubsub_topic" "bqjobcompleted" {
  provider = google-beta
  name     = "topic-job-completed"
  project  = var.project
}

# -- receive notifications from bigquery jobs completed (at org-level)
resource "google_pubsub_subscription" "bqjobcompleted" {
  provider             = google-beta
  project  = var.project
  name                 = "sub-topic-job-completed"
  topic                = google_pubsub_topic.bqjobcompleted.id
  ack_deadline_seconds = 600

}


resource "google_storage_notification" "notification" {
  bucket         = google_storage_bucket.bucket.name
  payload_format = "JSON_API_V1"
  topic          = google_pubsub_topic.bqjobcompleted.id
  event_types    = ["OBJECT_FINALIZE", "OBJECT_METADATA_UPDATE"]
  depends_on = [google_pubsub_topic_iam_binding.binding]
}
