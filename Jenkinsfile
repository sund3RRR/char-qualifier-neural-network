pipeline {
    agent {
        docker {
            image 'python:3.11.5-bookworm'
        }
    }
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Build environment') {
            steps {
                dir('app/char-qualifier-neural-network') {
                    sh 'Building virtual environment'

                    sh 'virtualenv --python=/usr/bin/python venv'
                    sh 'export TERM="linux"'
                    sh 'pip install -r requirements.txt'

                    sh 'echo Building environment success'
                }
            }
        }
        stage('Lint') {
            steps {
                sh 'Starting pylint'
                sh 'pylint --rcfile=pylint.cfg funniest/ $(find . -maxdepth 1 -name "*.py" -print) \
                    --msg-template="{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}" > pylint.log  \
                    || echo "pylint exited with $?"'
            }
        }
        stage('Test') {
            steps {
                sh 'echo "Running tests"'
                sh 'python3 manage.py test'
            }
        }
        stage('Deploy') {
            agent {
                dockerfile {
                    filename 'Dockerfile'
                    dir env.WORKSPACE + '/app'
                }
            }
            steps {
                sh 'echo "Deploying..."'
            }
        }
    }
}
