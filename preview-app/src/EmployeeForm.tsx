import React, { useState } from 'react';
import type { Employee } from './types';

interface Props {
  employee?: Employee;
  onSubmit: (employee: Employee) => void;
}

const EmployeeForm: React.FC<Props> = ({ employee, onSubmit }) => {
  const [id, setId] = useState(employee?.id ?? '');
  const [firstName, setFirstName] = useState(employee?.firstName ?? '');
  const [lastName, setLastName] = useState(employee?.lastName ?? '');
  const [email, setEmail] = useState(employee?.email ?? '');
  const [department, setDepartment] = useState<Employee['department'] | ''>(employee?.department ?? '');
  const [role, setRole] = useState<Employee['role'] | ''>(employee?.role ?? '');
  const [salary, setSalary] = useState(employee?.salary ?? 0);
  const [startDate, setStartDate] = useState(employee?.startDate ?? '');
  const [isActive, setIsActive] = useState(employee?.isActive ?? false);
  const [address, setAddress] = useState<Employee['address']>(employee?.address ?? { city: '', country: '' });
  const [skills, setSkills] = useState(employee?.skills ?? []);

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const newEmployee: Employee = {
      id,
      firstName,
      lastName,
      email,
      department: department as Employee['department'],
      role: role as Employee['role'],
      salary,
      startDate,
      isActive,
      address,
      skills,
    };
    onSubmit(newEmployee);
  };

  return (
    <form onSubmit={handleSubmit} className='max-w-sm mx-auto mb-8 rounded-lg bg-white p-4 shadow-md'>
      <div className='mb-4'>
        <label className='block text-gray-700 text-sm font-bold mb-2' htmlFor='id'>ID *</label>
        <input className='appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline' id='id' type='text' value={id} onChange={(event) => setId(event.target.value)} />
      </div>
      <div className='mb-4'>
        <label className='block text-gray-700 text-sm font-bold mb-2' htmlFor='firstName'>First Name *</label>
        <input className='appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline' id='firstName' type='text' value={firstName} onChange={(event) => setFirstName(event.target.value)} />
      </div>
      <div className='mb-4'>
        <label className='block text-gray-700 text-sm font-bold mb-2' htmlFor='lastName'>Last Name *</label>
        <input className='appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline' id='lastName' type='text' value={lastName} onChange={(event) => setLastName(event.target.value)} />
      </div>
      <div className='mb-4'>
        <label className='block text-gray-700 text-sm font-bold mb-2' htmlFor='email'>Email *</label>
        <input className='appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline' id='email' type='email' value={email} onChange={(event) => setEmail(event.target.value)} />
      </div>
      <div className='mb-4'>
        <label className='block text-gray-700 text-sm font-bold mb-2' htmlFor='department'>Department *</label>
        <select className='block appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline' id='department' value={department} onChange={(event) => setDepartment(event.target.value as Employee['department'] | '')}>
          <option value=''>Select Department</option>
          <option value='Engineering'>Engineering</option>
          <option value='Design'>Design</option>
          <option value='Marketing'>Marketing</option>
          <option value='HR'>HR</option>
          <option value='Finance'>Finance</option>
        </select>
      </div>
      <div className='mb-4'>
        <label className='block text-gray-700 text-sm font-bold mb-2' htmlFor='role'>Role *</label>
        <select className='block appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline' id='role' value={role} onChange={(event) => setRole(event.target.value as Employee['role'] | '')}>
          <option value=''>Select Role</option>
          <option value='junior'>Junior</option>
          <option value='mid'>Mid</option>
          <option value='senior'>Senior</option>
          <option value='lead'>Lead</option>
          <option value='manager'>Manager</option>
        </select>
      </div>
      <div className='mb-4'>
        <label className='block text-gray-700 text-sm font-bold mb-2' htmlFor='salary'>Salary</label>
        <input className='appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline' id='salary' type='number' value={salary} onChange={(event) => setSalary(Number(event.target.value))} />
      </div>
      <div className='mb-4'>
        <label className='block text-gray-700 text-sm font-bold mb-2' htmlFor='startDate'>Start Date</label>
        <input className='appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline' id='startDate' type='date' value={startDate} onChange={(event) => setStartDate(event.target.value)} />
      </div>
      <div className='mb-4'>
        <label className='block text-gray-700 text-sm font-bold mb-2' htmlFor='isActive'>Is Active</label>
        <input className='appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline' id='isActive' type='checkbox' checked={isActive} onChange={(event) => setIsActive(event.target.checked)} />
      </div>
      <div className='mb-4'>
        <label className='block text-gray-700 text-sm font-bold mb-2' htmlFor='addressStreet'>Address Street</label>
        <input className='appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline' id='addressStreet' type='text' value={address.street ?? ''} onChange={(event) => setAddress({ ...address, street: event.target.value })} />
      </div>
      <div className='mb-4'>
        <label className='block text-gray-700 text-sm font-bold mb-2' htmlFor='addressCity'>Address City *</label>
        <input className='appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline' id='addressCity' type='text' value={address.city} onChange={(event) => setAddress({ ...address, city: event.target.value })} />
      </div>
      <div className='mb-4'>
        <label className='block text-gray-700 text-sm font-bold mb-2' htmlFor='addressCountry'>Address Country *</label>
        <input className='appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline' id='addressCountry' type='text' value={address.country} onChange={(event) => setAddress({ ...address, country: event.target.value })} />
      </div>
      <div className='mb-4'>
        <label className='block text-gray-700 text-sm font-bold mb-2' htmlFor='skills'>Skills</label>
        <input className='appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline' id='skills' type='text' value={skills.join(', ')} onChange={(event) => setSkills(event.target.value.split(', '))} />
      </div>
      <button className='bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded' type='submit'>Submit</button>
    </form>
  );
};

export default EmployeeForm;