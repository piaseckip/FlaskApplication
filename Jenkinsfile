pipeline{
    options {
        timestamps()
    }
    agent any

    stages{

        stage('Checkout'){
            steps{
                deleteDir()
                checkout scm
                withCredentials([string(credentialsId: 'api_token', variable: 'TOKEN')]) { 
                    sh "git fetch http://jenkins:$TOKEN@35.178.81.143/piaseckip/FlaskApplication --tags"
                }

            }
        }               
        
        stage('Build'){
            when{
                anyOf{
                    branch "master"
                }
            }
            steps{
                sh "docker-compose up --build -d"
            }
        }

        stage('Test'){
            when{
                anyOf{
                    branch "master"
                }
            }
            steps{
                sleep 10
                sh "curl -i localhost:5001 | grep 200"
            }
        }
        // stage('Create image'){
        //     when{
        //         anyOf{
        //             branch "master"
        //         }
        //     }
        //     steps{
        //         sh "dokcer image ls"
        //         sh "dokcer commit nginx"
        //     }
        // }
        
        stage('Deploy'){
            when{
                anyOf{
                    branch "master"
                }
            }
            steps{
                sh "aws ecr get-login-password --region eu-west-3 | docker login --username AWS --password-stdin 644435390668.dkr.ecr.eu-west-3.amazonaws.com"
                sh "docker push 644435390668.dkr.ecr.eu-west-3.amazonaws.com/pp_nginx:latest"
                sh "docker push 644435390668.dkr.ecr.eu-west-3.amazonaws.com/pp_flask_app:latest"

            }
        }

    
    }
    
}