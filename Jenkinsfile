pipeline {
    agent any

    environment {
        APP_NAME = "securedev-app"
        DOCKER_NET = "securedev-net"
    }

    stages {
        stage('1. Construccion (Build)') {
            steps {
                sh "docker build -t ${APP_NAME}:${BUILD_NUMBER} -t ${APP_NAME}:latest ."
            }
        }

        stage('2. Pruebas Unitarias (Test)') {
            steps {
                sh "docker run --rm ${APP_NAME}:${BUILD_NUMBER} python -m unittest discover -v"
            }
        }

        stage('3. Revision de Seguridad SAST (Bandit)') {
            steps {
                sh '''
                    python3 -m venv /tmp/sast-venv
                    /tmp/sast-venv/bin/pip install -q bandit
                    /tmp/sast-venv/bin/bandit -r app.py -f txt -o bandit_report.txt || true
                    cat bandit_report.txt
                '''
            }
        }

        stage('4. Despliegue (Deploy)') {
            steps {
                sh """
                    docker rm -f ${APP_NAME} || true
                    docker run -d --name ${APP_NAME} --network ${DOCKER_NET} -p 5000:5000 ${APP_NAME}:latest
                    sleep 3
                    curl -f "http://${APP_NAME}:5000/hello?name=HealthCheck"
                """
            }
        }

        stage('5. Pruebas de Seguridad DAST (OWASP ZAP)') {
            steps {
                sh """
                    docker rm -f zap-scan || true
                    docker run --name zap-scan --network ${DOCKER_NET} -u root ghcr.io/zaproxy/zaproxy:stable sh -c "mkdir -p /zap/wrk && zap-full-scan.py -t 'http://${APP_NAME}:5000/hello?name=test' -m 1 -r zap_report.html -J zap_report.json || true"
                    docker cp zap-scan:/zap/wrk/zap_report.html ./zap_report.html
                    docker cp zap-scan:/zap/wrk/zap_report.json ./zap_report.json
                    docker rm -f zap-scan || true
                """
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'bandit_report.txt, zap_report.html, zap_report.json', allowEmptyArchive: true
        }
    }
}
