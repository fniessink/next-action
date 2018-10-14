pipeline {
    agent any
    stages {
        stage('Unit tests') {
            steps {
                sh 'cd next-action; docker-compose -f docker-compose.yml -f docker-compose.jenkins.yml up unittest'
                publishHTML target: [
                    allowMissing: false,
                    alwaysLinkToLastBuild: true,
                    keepAll: false,
                    reportDir: 'next-action/build/unittest-coverage',
                    reportFiles: 'index.html',
                    reportName: 'Unit test coverage report'
                ]
            }
        }
        stage('Feature tests') {
            steps {
                sh 'cd next-action; docker-compose -f docker-compose.yml -f docker-compose.jenkins.yml up behave'
                publishHTML target: [
                    allowMissing: false,
                    alwaysLinkToLastBuild: true,
                    keepAll: false,
                    reportDir: 'next-action/build/feature-coverage',
                    reportFiles: 'index.html',
                    reportName: 'Feature test coverage report'
                ]
            }
        }
        stage('Security checks') {
            steps {
                sh 'cd next-action; docker-compose -f docker-compose.yml -f docker-compose.jenkins.yml up security owasp-dependency-check'
                publishHTML target: [
                    allowMissing: false,
                    alwaysLinkToLastBuild: true,
                    keepAll: false,
                    reportDir: 'next-action/build',
                    reportFiles: 'bandit.html',
                    reportName: 'Bandit report'
                ]
                publishHTML target: [
                    allowMissing: false,
                    alwaysLinkToLastBuild: true,
                    keepAll: false,
                    reportDir: 'owasp-dependency-check-report',
                    reportFiles: 'dependency-check-report.html',
                    reportName: 'OWASP dependency check report'
                ]
            }
        }
        stage('Quality checks') {
            steps {
                sh 'cd next-action; docker-compose -f docker-compose.yml -f docker-compose.jenkins.yml up quality sonarqube-scanner'
                publishHTML target: [
                    allowMissing: false,
                    alwaysLinkToLastBuild: true,
                    keepAll: false,
                    reportDir: 'next-action/build/mypy',
                    reportFiles: 'index.html',
                    reportName: 'Mypy report'
                ]
            }
        }
        stage('Documentation') {
            steps {
                sh 'cd next-action; docker-compose -f docker-compose.yml -f docker-compose.jenkins.yml up docs'
                publishHTML target: [
                    allowMissing: false,
                    alwaysLinkToLastBuild: true,
                    keepAll: false,
                    reportDir: 'next-action/build/',
                    reportFiles: 'README.html',
                    reportName: 'README'
                ]
            }
        }
    }
}
