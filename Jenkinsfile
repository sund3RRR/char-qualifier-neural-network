pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Build environment') {
            steps {
                dir('app/char-qualifier-neural-network') {
                    sh 'echo "Building virtual environment"'

                    sh 'virtualenv --python=/usr/bin/python3 venv'
                    sh 'export TERM="linux"'
                    sh '''
                    . .venv/bin/activate
                    pip install -r requirements.txt
                    '''

                    sh 'echo "Building environment success"'
                }
            }
        }
        stage('Lint') {
            steps {
                sh 'Starting pylint'
                sh '''
                . .venv/bin/activate
                pylint --rcfile=pylint.cfg funniest/ $(find . -maxdepth 1 -name "*.py" -print) \
                    --msg-template="{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}" > pylint.log  \
                    || echo "pylint exited with $?"'''
            }
        }
        stage('Test') {
            steps {
                sh 'echo "Running tests"'
                sh '''
                . .venv/bin/activate
                python3 manage.py test
                '''
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
