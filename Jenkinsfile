pipeline {
    agent any 
    stages {
        stage('Stage unit tests') {
            steps {
                sh 'docker-compose -f docker-compose.yml -f docker-compose.jenkins.yml up unittest'
                publishHTML target: [
                    allowMissing: false,
                    alwaysLinkToLastBuild: true,
                    keepAll: false,
                    reportDir: 'build/unittest-coverage',
                    reportFiles: 'index.html',
                    reportName: 'Unit test coverage report'
                ]
            }
        }
        stage('Stage feature tests') {
            steps {
                sh 'docker-compose -f docker-compose.yml -f docker-compose.jenkins.yml up behave'
                publishHTML target: [
                    allowMissing: false,
                    alwaysLinkToLastBuild: true,
                    keepAll: false,
                    reportDir: 'build/feature-coverage',
                    reportFiles: 'index.html',
                    reportName: 'Feature test coverage report'
                ]
            }
        }
    }
}
