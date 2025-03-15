FROM nginx:1.23.1

RUN apt-get update && apt-get install -y unzip curl

ADD https://github.com/open-telemetry/opentelemetry-cpp-contrib/releases/download/webserver%2Fv1.0.3/opentelemetry-webserver-sdk-x64-linux.tgz /opt
RUN cd /opt && tar xvzf opentelemetry-webserver-sdk-x64-linux.tgz
RUN cd /opt/opentelemetry-webserver-sdk && ./install.sh

ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/opentelemetry-webserver-sdk/sdk_lib/lib

# ✅ Inject OpenTelemetry module cleanly
RUN sed -i '1iload_module /opt/opentelemetry-webserver-sdk/WebServerModule/Nginx/1.23.1/ngx_http_opentelemetry_module.so;' /etc/nginx/nginx.conf

# ✅ Copy your app config
COPY opentelemetry_module.conf /etc/nginx/conf.d/
COPY nginx.conf /etc/nginx/conf.d/default.conf
