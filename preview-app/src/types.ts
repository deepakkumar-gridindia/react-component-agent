export interface Address {
  street?: string;
  city: string;
  country: string;
}

export interface Employee {
  id: string;
  firstName: string;
  lastName: string;
  email: string;
  department: 'Engineering' | 'Design' | 'Marketing' | 'HR' | 'Finance';
  role: 'junior' | 'mid' | 'senior' | 'lead' | 'manager';
  salary: number;
  startDate: string;
  isActive: boolean;
  address: Address;
  skills: string[];
}