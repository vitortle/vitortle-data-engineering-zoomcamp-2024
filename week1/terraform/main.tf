terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "6.14.1"
    }
  }
}

provider "google" {
  project = "sublime-cargo-444816-q5"
  region  = "us-central1"
}

resource "google_storage_bucket" "demo-bucket" {
  name          = "sublime-cargo-444816-q5-terra-bucket"
  location      = "US"
  force_destroy = true

  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}