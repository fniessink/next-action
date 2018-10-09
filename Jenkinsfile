pipeline {
    agent any
    stages {
        stage('Unit tests') {
            steps {
                sh 'cd src; docker-compose -f docker-compose.yml -f docker-compose.jenkins.yml up unittest'
                publishHTML target: [
                    allowMissing: false,
                    alwaysLinkToLastBuild: true,
                    keepAll: false,
                    reportDir: 'src/build/unittest-coverage',
                    reportFiles: 'index.html',
                    reportName: 'Unit test coverage report'
                ]
            }
        }
        stage('Feature tests') {
            steps {
                sh 'cd src; docker-compose -f docker-compose.yml -f docker-compose.jenkins.yml up behave'
                publishHTML target: [
                    allowMissing: false,
                    alwaysLinkToLastBuild: true,
                    keepAll: false,
                    reportDir: 'src/build/feature-coverage',
                    reportFiles: 'index.html',
                    reportName: 'Feature test coverage report'
                ]
            }
        }
        stage('Security checks') {
            steps {
                sh 'cd src; docker-compose -f docker-compose.yml -f docker-compose.jenkins.yml up bandit'
                publishHTML target: [
                    allowMissing: false,
                    alwaysLinkToLastBuild: true,
                    keepAll: false,
                    reportDir: 'src/build',
                    reportFiles: 'bandit.html',
                    reportName: 'Bandit report'
                ]
                sh 'cd src; docker-compose -f docker-compose.yml -f docker-compose.jenkins.yml up owasp-dependency-check'
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
                sh 'cd src; docker-compose -f docker-compose.yml -f docker-compose.jenkins.yml up mypy pylint pydocstyle pycodestyle vulture pyroma'
                publishHTML target: [
                    allowMissing: false,
                    alwaysLinkToLastBuild: true,
                    keepAll: false,
                    reportDir: 'src/build/mypy',
                    reportFiles: 'index.html',
                    reportName: 'Mypy report'
                ]
            }
        }
    }
}
