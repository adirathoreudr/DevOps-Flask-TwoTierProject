pipeline{
    agent any
    stages{
        stage('Clone repo'){
            steps{
                git branch: 'main', url: 'https://github.com/adirathoreudr/DevOps_Flask_TwoTIerProject.git'
            }
        }

       stage('Cleanup') {
    steps {
        sh '''
        docker compose down --volumes --remove-orphans || true
        docker rm -f $(docker ps -aq) || true
        '''
    }
}
        stage('Build image'){
            steps{
                sh 'docker build -t flask-app .'
            }
        }
        stage('Deploy with docker compose'){
            steps{
                // existing container if they are running
                sh 'docker compose down || true'
                // start app, rebuilding flask image
                sh 'docker compose up -d --build'
            }
        }
        stage('Train Model') {
    steps {
        sh 'python3 model/train_model.py'
    }
}
    }
}