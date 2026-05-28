# S3 Bucket - intentional security issues
resource "aws_s3_bucket" "my_bucket" {
  bucket = "my-sample-bucket"
}

resource "aws_s3_bucket_acl" "my_bucket_acl" {
  bucket = aws_s3_bucket.my_bucket.id
  acl    = "public-read"
}

# CloudFront Distribution - intentional CDN issues
resource "aws_cloudfront_distribution" "my_distribution" {
  enabled = true

  origin {
    domain_name = aws_s3_bucket.my_bucket.bucket_regional_domain_name
    origin_id   = "S3Origin"
  }

  default_cache_behavior {
    allowed_methods        = ["GET", "HEAD"]
    cached_methods         = ["GET", "HEAD"]
    target_origin_id       = "S3Origin"
    viewer_protocol_policy = "allow-all"

    forwarded_values {
      query_string = false
      cookies {
        forward = "none"
      }
    }
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    cloudfront_default_certificate = true
  }
}

# EC2 Instance - intentional cost issue
resource "aws_instance" "my_instance" {
  ami           = "ami-0abcdef1234567890"
  instance_type = "t3.2xlarge"
}
