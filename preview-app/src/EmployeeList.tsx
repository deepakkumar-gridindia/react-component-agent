import React from 'react';
import type { Employee } from './types';
import EmployeeCard from './EmployeeCard';

interface Props {
  employees: Employee[];
}

const EmployeeList: React.FC<Props> = ({ employees }) => {
  return (
    <div className='flex flex-wrap justify-center mb-8'>
      {employees.map((employee) => (
        <EmployeeCard key={employee.id} employee={employee} />
      ))}
    </div>
  );
};

export default EmployeeList;