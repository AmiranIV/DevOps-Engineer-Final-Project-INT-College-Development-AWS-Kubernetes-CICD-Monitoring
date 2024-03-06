FROM ubuntu:latest as installer

RUN apt-get update && apt-get install curl -y

# Install AWS CLI
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" \
    && apt-get install -y unzip \
    && unzip awscliv2.zip \
    && ./aws/install --bin-dir /aws-cli-bin/

# Install Snyk CLI
RUN mkdir /snyk && cd /snyk \
    && curl https://static.snyk.io/cli/v1.666.0/snyk-linux -o snyk \
    && chmod +x ./snyk

# Install yq
RUN curl -L https://github.com/mikefarah/yq/releases/download/3.4.1/yq_linux_amd64 -o /usr/bin/yq \
    && chmod +x /usr/bin/yq

FROM jenkins/agent

# Copy Docker client binary
COPY --from=docker /usr/local/bin/docker /usr/local/bin/

# Copy AWS CLI and Snyk CLI
COPY --from=installer /usr/local/aws-cli/ /usr/local/aws-cli/
COPY --from=installer /aws-cli-bin/ /usr/local/bin/
COPY --from=installer /snyk/ /usr/local/bin/
