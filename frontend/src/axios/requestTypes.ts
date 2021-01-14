export interface Credentials {
    email: string,
    password: string,
}

export interface NewCredentials extends Credentials {
    passwordConfirm: string,
}
