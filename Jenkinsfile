pipeline {
    agent any
    stages {
        stage('Unit tests') {
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
        stage('Feature tests') {
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
        stage('Security checks') {
            steps {
                sh 'docker-compose -f docker-compose.yml -f docker-compose.jenkins.yml up bandit'
                publishHTML target: [
                    allowMissing: false,
                    alwaysLinkToLastBuild: true,
                    keepAll: false,
                    reportDir: 'build',
                    reportFiles: 'bandit.html',
                    reportName: 'Bandit report'
                ]
                sh 'docker-compose -f docker-compose.yml -f docker-compose.jenkins.yml up owasp-dependency-check'
                publishHTML target: [
                    allowMissing: false,
                    alwaysLinkToLastBuild: true,
                    keepAll: false,
                    reportDir: 'build/owasp-dependency-check-report',
                    reportFiles: 'dependency-check-report.html',
                    reportName: 'OWASP dependency check report'
                ]
            }
        }
        stage('Quality checks') {
            steps {
                sh 'docker-compose -f docker-compose.yml -f docker-compose.jenkins.yml up mypy pylint'
                publishHTML target: [
                    allowMissing: false,
                    alwaysLinkToLastBuild: true,
                    keepAll: false,
                    reportDir: 'build/mypy',
                    reportFiles: 'index.html',
                    reportName: 'Mypy report'
                ]
            }
        }
    }
}
