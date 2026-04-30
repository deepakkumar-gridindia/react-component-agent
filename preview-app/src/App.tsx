import { useState } from 'react'
import './index.css'
import EmployeeCard from './EmployeeCard'
import EmployeeForm from './EmployeeForm'
import EmployeeList from './EmployeeList'

const SAMPLE_EMPLOYEES = [
  {
    id: '1',
    firstName: 'Alice',
    lastName: 'Johnson',
    email: 'alice@example.com',
    department: 'Engineering' as const,
    role: 'senior' as const,
    salary: 120000,
    startDate: '2021-03-15',
    isActive: true,
    address: { street: '123 Main St', city: 'San Francisco', country: 'USA' },
    skills: ['TypeScript', 'React', 'Node.js'],
  },
  {
    id: '2',
    firstName: 'Bob',
    lastName: 'Smith',
    email: 'bob@example.com',
    department: 'Design' as const,
    role: 'mid' as const,
    salary: 95000,
    startDate: '2022-07-01',
    isActive: true,
    address: { city: 'New York', country: 'USA' },
    skills: ['Figma', 'Tailwind', 'CSS'],
  },
]

type Tab = 'card' | 'list' | 'form'

export default function App() {
  const [tab, setTab] = useState<Tab>('card')

  const tabClass = (t: Tab) =>
    `px-4 py-2 rounded-t-lg font-medium transition-colors ${
      tab === t
        ? 'bg-white text-blue-600 border border-b-white border-gray-200'
        : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
    }`

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <h1 className="text-3xl font-bold text-gray-800 mb-2">
        Generated Components Preview
      </h1>
      <p className="text-gray-500 mb-8">Employee schema · React + TypeScript + Tailwind</p>

      {/* Tab bar */}
      <div className="flex gap-1 mb-0">
        <button className={tabClass('card')} onClick={() => setTab('card')}>EmployeeCard</button>
        <button className={tabClass('list')} onClick={() => setTab('list')}>EmployeeList</button>
        <button className={tabClass('form')} onClick={() => setTab('form')}>EmployeeForm</button>
      </div>

      <div className="bg-white border border-gray-200 rounded-b-lg rounded-tr-lg p-6 shadow-sm">
        {tab === 'card' && (
          <div>
            <p className="text-sm text-gray-400 mb-4">Rendering first sample employee</p>
            <EmployeeCard employee={SAMPLE_EMPLOYEES[0]} />
          </div>
        )}
        {tab === 'list' && (
          <div>
            <p className="text-sm text-gray-400 mb-4">Rendering both sample employees</p>
            <EmployeeList employees={SAMPLE_EMPLOYEES} />
          </div>
        )}
        {tab === 'form' && (
          <div>
            <p className="text-sm text-gray-400 mb-4">Empty create form</p>
            <EmployeeForm onSubmit={(e) => alert(`Submitted: ${e.firstName} ${e.lastName}`)} />
          </div>
        )}
      </div>
    </div>
  )
}
