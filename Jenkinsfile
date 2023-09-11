pipeline {
    agent {
        dockerfile {
            filename 'Dockerfile'
            dir 'app'
        }
    }
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Test') {
            steps {
                dir ('app/char-qualifier-neural-network') {
                    sh 'echo "Running tests"'
                    sh 'python3 manage.py tests'
                }
            }
        }
    }
}
