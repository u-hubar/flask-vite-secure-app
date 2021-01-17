export interface Tokens { 
  access: string;
  refresh: string;
}

export interface Service {
  id: number,
  service: string;
  url: string;
  username: string;
}

export interface servicePassword {
  password: string;
}
