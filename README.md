# Project Description (Work in progress)

KubeCommerce is a cloud-native e-commerce application built to demonstrate production-level DevOps and platform engineering practices. The application provides a realistic distributed workload composed of a checkout API written in Python/FastAPI, and a Go payment service. The services generate structured logs, metrics, and distributed traces while processing checkout and simulated payment requests, including successful transactions, declines, delays, and failures.

The platform is containerized with Docker and deployed to Kubernetes with Helm. The underlying infrastructure is provisioned through Terraform. Github Actions automates testing, security scanning, image creation, and deployment. In regards to observability, I use Prometheus, Grafana, and OpenTelemetry. On the Kubernetes side, I use health probes, resource limits, autoscaling, RBAC, NetworkPolicies, and Gateway API resources to demonstrate production-oriented reliability and security.

To test the functionality of each of the components, and to practice monitoring, alerting, and troubleshooting, I induce controlled failures. Failures consist of database outages, payment errors, increased latency, CPU saturation, and queue backlogs.

# Lessons Learned

- Idempotency in FastAPI. If a client loses connection before receiving a response, it can resend the exact same request with the same key. This could have unwanted results. Added a required idempotency key as part of the create checkout header