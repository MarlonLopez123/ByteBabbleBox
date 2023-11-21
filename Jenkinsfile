pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                script {
                    sh 'docker build -t chat-app .'
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    sh 'docker run chat-app python test.py'  # Ajusta el comando según tus necesidades
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    sh 'docker-compose up -d'  # Ajusta el comando según tus necesidades
                }
            }
        }
    }
}
