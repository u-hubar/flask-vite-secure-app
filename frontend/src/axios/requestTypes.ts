export interface Credentials {
    email: string,
    username: string,
    password: string,
}

export interface NewCredentials extends Credentials {
    passwordConfirm: string
}
