# ======================================================================================== #
#    _____                  __                __      __       _   _              _
#   |_   _|__ _ _ _ _ __ _ / _|___ _ _ _ __   \ \    / /__ _ _| |_| |___  __ _ __| |
#     | |/ -_) '_| '_/ _` |  _/ _ \ '_| '  \   \ \/\/ / _ \ '_| / / / _ \/ _` / _` |
#     |_|\___|_| |_| \__,_|_| \___/_| |_|_|_|   \_/\_/\___/_| |_\_\_\___/\__,_\__,_|
#
# ======================================================================================== #

# technical BigQuery
resource "google_bigquery_dataset" "servierdataset" {
  provider      = google-beta
  project       = var.project
  dataset_id    = "servier_technical_test"
  friendly_name = "Servier technical test"
  description   = "Dataset for servier technical test"
  location      = "EU"
}

resource "google_bigquery_table" "drugs_table" {
  provider    = google-beta
  project     = var.project
  dataset_id  = google_bigquery_dataset.servierdataset.dataset_id
  table_id    = "drugs"
  description = "Drugs table"

  schema = <<EOF
[
  {
    "name": "atccode",
    "type": "STRING",
    "mode": "REQUIRED",
    "description": "atc code"
  },
  {
    "name": "drug",
    "type": "STRING",
    "mode": "REQUIRED",
    "description": "drug name"
  }
]
EOF
}

resource "google_bigquery_table" "pubmed_table" {
  provider    = google-beta
  project     = var.project
  dataset_id  = google_bigquery_dataset.servierdataset.dataset_id
  table_id    = "pubmed"
  description = "pubmed table"

  schema = <<EOF
[
  {
    "name": "id",
    "type": "INTEGER",
    "mode": "NULLABLE",
    "description": "ID"
  },
  {
    "name": "title",
    "type": "STRING",
    "mode": "NULLABLE",
    "description": "title"
  },
  {
    "name": "date",
    "type": "DATE",
    "mode": "NULLABLE",
    "description": "title"
  },
  {
    "name": "journal",
    "type": "STRING",
    "mode": "NULLABLE",
    "description": "title"
  }
]
EOF
}

resource "google_bigquery_table" "clinicaltrials_table" {
  provider    = google-beta
  project     = var.project
  dataset_id  = google_bigquery_dataset.servierdataset.dataset_id
  table_id    = "clinical_trials"
  description = "clinical trials table"

  schema = <<EOF
[
  {
    "name": "id",
    "type": "STRING",
    "mode": "REQUIRED",
    "description": "ID"
  },
  {
    "name": "scientific_title",
    "type": "STRING",
    "mode": "REQUIRED",
    "description": "scientific title"
  },
  {
    "name": "date",
    "type": "DATE",
    "mode": "REQUIRED",
    "description": "date"
  },
  {
    "name": "journal",
    "type": "STRING",
    "mode": "REQUIRED",
    "description": "journal"
  }
]
EOF
}


resource "google_bigquery_table" "output" {
  provider    = google-beta
  project     = var.project
  dataset_id  = google_bigquery_dataset.servierdataset.dataset_id
  table_id    = "output"
  description = "output table"

  schema = <<EOF
[
  {
    "name": "id",
    "type": "STRING",
    "mode": "REQUIRED",
    "description": "ID"
  },
  {
    "name": "drug",
    "type": "STRING",
    "mode": "REQUIRED",
    "description": "scientific title"
  },
  {
    "name": "date",
    "type": "DATE",
    "mode": "REQUIRED",
    "description": "date"
  },
  {
    "name": "journal",
    "type": "STRING",
    "mode": "REQUIRED",
    "description": "journal"
  }
]
EOF
}