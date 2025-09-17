import { useState } from 'react'

function App() {
  const [branches] = useState([
    "release-1.0", 
    "release-2.0", 
    "release-3.0", 
    "release-4.0", 
    "release-5.0"
  ])
  const [logs, setLogs] = useState([])
  const [isRunning, setIsRunning] = useState(false)

  const simulateScriptExecution = () => {
    setIsRunning(true)
    setLogs([])
    
    // Simulate the bash script execution
    branches.forEach((branch, index) => {
      setTimeout(() => {
        setLogs(prevLogs => [
          ...prevLogs,
          `✓ Checked out branch: ${branch}`,
          `✓ Created file: ${branch}.txt`,
          `✓ Committed changes to ${branch}`,
          `✓ Pushed to origin/${branch}`,
          '---'
        ])
        
        if (index === branches.length - 1) {
          setTimeout(() => {
            setLogs(prevLogs => [...prevLogs, '🎉 Script execution completed!'])
            setIsRunning(false)
          }, 500)
        }
      }, (index + 1) * 1000)
    })
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-8 px-4">
      <div className="max-w-4xl mx-auto">
        <div className="bg-white rounded-lg shadow-xl p-8">
          <div className="text-center mb-8">
            <h1 className="text-4xl font-bold text-gray-800 mb-2">
              Git Branch Manager
            </h1>
            <p className="text-gray-600">
              Web interface for managing multiple git release branches
            </p>
          </div>

          <div className="grid md:grid-cols-2 gap-8">
            {/* Branch List */}
            <div className="bg-gray-50 rounded-lg p-6">
              <h2 className="text-2xl font-semibold text-gray-800 mb-4">
                Release Branches
              </h2>
              <div className="space-y-3">
                {branches.map((branch, index) => (
                  <div 
                    key={branch}
                    className="flex items-center justify-between bg-white p-3 rounded-md shadow-sm"
                  >
                    <span className="font-medium text-gray-700">{branch}</span>
                    <span className="text-sm bg-blue-100 text-blue-800 px-2 py-1 rounded">
                      Release
                    </span>
                  </div>
                ))}
              </div>
              
              <button
                onClick={simulateScriptExecution}
                disabled={isRunning}
                className={`w-full mt-6 py-3 px-4 rounded-md font-medium transition-colors ${
                  isRunning 
                    ? 'bg-gray-400 cursor-not-allowed text-white'
                    : 'bg-blue-600 hover:bg-blue-700 text-white'
                }`}
              >
                {isRunning ? 'Running Script...' : 'Execute Git Script'}
              </button>
            </div>

            {/* Execution Logs */}
            <div className="bg-gray-900 rounded-lg p-6">
              <h2 className="text-2xl font-semibold text-white mb-4">
                Execution Logs
              </h2>
              <div className="bg-black rounded p-4 h-80 overflow-y-auto font-mono text-sm">
                {logs.length === 0 ? (
                  <p className="text-green-400">Ready to execute script...</p>
                ) : (
                  logs.map((log, index) => (
                    <div key={index} className="text-green-400 mb-1">
                      {log}
                    </div>
                  ))
                )}
              </div>
            </div>
          </div>

          {/* Script Overview */}
          <div className="mt-8 bg-blue-50 rounded-lg p-6">
            <h3 className="text-xl font-semibold text-gray-800 mb-3">
              What this script does:
            </h3>
            <ul className="space-y-2 text-gray-700">
              <li className="flex items-center">
                <span className="w-2 h-2 bg-blue-500 rounded-full mr-3"></span>
                Loops through each release branch
              </li>
              <li className="flex items-center">
                <span className="w-2 h-2 bg-blue-500 rounded-full mr-3"></span>
                Checks out the branch
              </li>
              <li className="flex items-center">
                <span className="w-2 h-2 bg-blue-500 rounded-full mr-3"></span>
                Creates a file named after the branch
              </li>
              <li className="flex items-center">
                <span className="w-2 h-2 bg-blue-500 rounded-full mr-3"></span>
                Commits and pushes changes to the branch
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  )
}

export default App
