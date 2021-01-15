export interface Credentials {
    email: string,
    password: string,
}

export interface NewCredentials extends Credentials {
    passwordConfirm: string,
}


export interface MasterCredentials {
    master: string
}


export interface NewMasterCredentials extends MasterCredentials {
    masterConfirm: string,
}


export interface NewService {
    service: string,
    url: string,
    username: string,
    password: string,
}
