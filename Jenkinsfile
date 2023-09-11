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
                    . ./venv/bin/activate
                    pip install -r requirements.txt
                    '''

                    sh 'echo "Building environment success"'
                }
            }
        }
        stage('Lint') {
            steps {
                dir('app/char-qualifier-neural-network') {
                    sh 'echo "Starting pylint"'

                    sh '''
                    . ./venv/bin/activate
                    find . -type f -name "*.py" | while read -r file; do
                        echo "Checking $file with pylint..."
                        pylint "$file"
                    done
                    '''

                    sh 'echo "Linting success"'
                }
            }
        }
        stage('Test') {
            steps {
                dir('app/char-qualifier-neural-network') {
                    sh 'echo "Running tests"'
                    sh '''
                    . ./venv/bin/activate
                    python3 manage.py test
                    '''
                }
            }
        }
        stage('Deploy') {
            agent {
                dockerfile {
                    filename 'Dockerfile'
                    dir 'app'
                }
            }
            steps {
                sh 'echo "Deploying..."'
            }
        }
    }
}
