SHELL := /bin/bash
k8s_namespace := eds

APP_LABEL := vllm-completion
LOCAL_PORT := 8000
REMOTE_PORT := 8000


# ---------------------------------------------------------------------
# Environment and secrets setup
# ---------------------------------------------------------------------
deploy_config:
	@echo "Creating ConfigMap and HF token secret in namespace $(k8s_namespace)..."
	-kubectl -n $(k8s_namespace) delete configmap librechat-env || true
	kubectl -n $(k8s_namespace) create configmap librechat-env --from-env-file=.env --dry-run=client -o yaml | kubectl apply -f -
	@set -a && \
	source .env && \
	kubectl create secret generic hf-token-secret \
	  --namespace=$(k8s_namespace) \
	  --from-literal=token=$${HF_TOKEN} \
	  --dry-run=client -o yaml | kubectl apply -n $(k8s_namespace) -f -

undeploy_config:
	@echo "Deleting configmap and HF token secret..."
	- kubectl -n $(k8s_namespace) delete configmap librechat-env || true
	- kubectl -n $(k8s_namespace) delete secret hf-token-secret || true

# ---------------------------------------------------------------------
# vLLM deployment
# ---------------------------------------------------------------------
deploy_llm:
	@echo "Deploying vLLM service..."
	kubectl -n $(k8s_namespace) apply -f llm/pvcs.yaml
	kubectl -n $(k8s_namespace) apply -f llm/vllm-completion-config.yaml
	kubectl -n $(k8s_namespace) apply -f llm/vllm-completion.yaml
	@echo "WARNING: VERFIY THE LLM IS READY BEFORE QUERYING AT: http://localhost:8000/v1/chat/completions"
	@echo "Waiting for LLM pod to ready..."
	@sleep 5
	@until kubectl -n $(k8s_namespace) logs -l app=$(APP_LABEL) | grep -q "Application startup complete"; do \
    	echo "Waiting for model load..."; sleep 60; \
	done
	@echo "Pod is ready. Starting port-forward to localhost:$(LOCAL_PORT)..."
	@POD=$$(kubectl -n $(k8s_namespace) get pod -l app=$(APP_LABEL) -o jsonpath="{.items[0].metadata.name}"); \
	echo "Forwarding $$POD"; \
	kubectl -n $(k8s_namespace) port-forward $$POD $(LOCAL_PORT):$(REMOTE_PORT)

undeploy_llm:
	@echo "Undeploying vLLM service (PVC retained)..."
	- kubectl -n $(k8s_namespace) delete -f llm/vllm-completion.yaml || true
	- kubectl -n $(k8s_namespace) delete -f llm/vllm-completion-config.yaml || true

# ---------------------------------------------------------------------
# Convenience targets
# ---------------------------------------------------------------------
deploy: deploy_config deploy_llm
undeploy: undeploy_llm undeploy_config

status:
	@echo "Pods in namespace $(k8s_namespace):"
	kubectl -n $(k8s_namespace) get pods -o wide

