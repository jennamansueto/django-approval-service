import axios from 'axios'

const apiClient = axios.create({
  baseURL: '/api',
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  },
})

export interface User {
  id: number
  username: string
  email: string
  role: string
}

export interface Client {
  id: number
  name: string
  created_at: string
  updated_at: string
}

export interface Deliverable {
  id: number
  title: string
  description: string
  client: number
  client_name: string
  status: string
  created_by: number
  created_by_username: string
  created_at: string
  updated_at: string
}

export interface ApprovalRequest {
  id: number
  deliverable: number
  deliverable_title: string
  requested_by: number
  requested_by_username: string
  status: string
  created_at: string
  decided_at: string | null
}

export const authApi = {
  login: (username: string, password: string) =>
    apiClient.post<User>('/auth/login/', { username, password }),
  logout: () => apiClient.post('/auth/logout/'),
  me: () => apiClient.get<User>('/auth/me/'),
}

export const clientsApi = {
  list: () => apiClient.get<Client[]>('/clients/'),
  create: (name: string) => apiClient.post<Client>('/clients/', { name }),
}

export const deliverablesApi = {
  list: () => apiClient.get<Deliverable[]>('/deliverables/'),
  create: (data: { title: string; description?: string; client: number }) =>
    apiClient.post<Deliverable>('/deliverables/', data),
  submit: (id: number) => apiClient.post<Deliverable>(`/deliverables/${id}/submit/`),
}

export const approvalsApi = {
  list: (status?: string) =>
    apiClient.get<ApprovalRequest[]>('/approvals/', { params: status ? { status } : {} }),
  approve: (id: number) => apiClient.post<ApprovalRequest>(`/approvals/${id}/approve/`),
  reject: (id: number) => apiClient.post<ApprovalRequest>(`/approvals/${id}/reject/`),
}

export default apiClient
