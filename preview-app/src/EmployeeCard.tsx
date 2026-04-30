import React from 'react';
import type { Employee } from './types';

interface Props {
  employee: Employee;
}

const EmployeeCard: React.FC<Props> = ({ employee }) => {
  return (
    <div className='max-w-sm mx-auto mb-8 rounded-lg bg-white p-4 shadow-md'>
      <h2 className='text-lg font-bold mb-2'>{employee.firstName} {employee.lastName}</h2>
      <p className='mb-2'>Email: {employee.email}</p>
      <p className='mb-2'>Department: <span className='badge'>{employee.department}</span></p>
      <p className='mb-2'>Role: <span className='badge'>{employee.role}</span></p>
      <p className='mb-2'>Salary: {employee.salary}</p>
      <p className='mb-2'>Start Date: {employee.startDate}</p>
      <p className='mb-2'>Active: {employee.isActive ? 'Yes' : 'No'}</p>
      <h3 className='text-lg font-bold mt-4 mb-2'>Address</h3>
      <p className='mb-2'>Street: {employee.address.street ?? '—'}</p>
      <p className='mb-2'>City: {employee.address.city}</p>
      <p className='mb-2'>Country: {employee.address.country}</p>
      <h3 className='text-lg font-bold mt-4 mb-2'>Skills</h3>
      <p className='mb-2'>{employee.skills.join(', ')}</p>
    </div>
  );
};

export default EmployeeCard;