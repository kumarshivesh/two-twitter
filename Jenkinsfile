pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                script {
                    checkout scm
                }
            }
        }

        // Comment out the other stages for now
        /*
        stage('Cleanup Previous Containers') {
            steps {
                script {
                    sh 'docker-compose down'
                }
            }
        }

        stage('Build and Test') {
            steps {
                script {
                    sh 'docker-compose build'
                    sh 'docker-compose run web python manage.py test'
                }
            }
        }

        stage('Deploy') {
            steps {
                script {
                    sh 'docker-compose up -d'
                }
            }
        }
        */
    }

    post {
        always {
            script {
                //sh 'echo "y" | docker system prune -a --volumes'
            }
        }
    }
}
