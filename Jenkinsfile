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
                sh 'echo "Running tests"'
                sh 'ls -la'
            }
        }
    }
}
