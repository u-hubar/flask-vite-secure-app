export interface Tokens { 
  access: string;
  refresh: string;
}

export interface Logs {
  datetime: string,
  user_agent: string,
  user_ip: string,
}

export interface Service {
  id: number,
  service: string;
  url: string;
  username: string;
  password?: string;
}

export interface ServicePassword {
  id: number;
  password: string;
}
