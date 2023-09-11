pipeline {
    agent {
        dockerfile {
            filename 'app/Dockerfile'
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
