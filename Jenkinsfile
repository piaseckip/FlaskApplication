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
                CMSG = sh(returnStdout: true, script: 'git log -1 --pretty=%B').trim()
                if ("${CMSG}".contains('/\d\.\d/')){
                    sh "echo ${CMSG}"  
                }

            }
        }

        // stage ('Calculate tag'){
        //     when {
        //         branch "master"
        //     }
        //     steps{
        //         script {
        //             BRANCH = env.BRANCH_NAME
                
        //             VERSION = sh(returnStdout: true, script: "echo '${BRANCH}' | cut -d '/' -f2 ").trim()
                    
        //             try {
        //                 LAST_TAG = sh(returnStdout: true, script: "git tag | sort -V | grep '${VERSION}' | tail -1 | cut -d '.' -f3").trim()

        //                 NEW_TAG = "${LAST_TAG}" as int

        //                 NEW_TAG = NEW_TAG + 1
        //             }

        //             catch (Exception e) {
        //                 NEW_TAG = 0
        //             }

        //             VERSION = "${VERSION}.${NEW_TAG}"
        //         } 
        // }             
        
        stage('Build'){
            steps{
                sh "docker-compose up --build -d"
            }
        }

        stage('Unit and Static Tests'){
            steps{
                sleep 10

                sh "curl -i localhost:5000 | grep 200"

                sh "curl -i localhost:5001 | grep 200"
            }
        }

        stage('Package'){
            steps{
                sh "echo package"
            }
        }

        stage('E2E test'){
            when{
                    branch "master"
                }
            }
            steps{
                sh "echo test"
            }
        }

        stage('Publish'){
            when{
                anyOf{
                    branch "master"
                }
            }
            steps{
                sh "echo publish"
            }
        }
        
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