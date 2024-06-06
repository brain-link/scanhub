/* tslint:disable */
/* eslint-disable */
/**
 * FastAPI
 * No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)
 *
 * The version of the OpenAPI document: 0.1.0
 * 
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 */


import type { Configuration } from './configuration';
import type { AxiosPromise, AxiosInstance, RawAxiosRequestConfig } from 'axios';
import globalAxios from 'axios';
// Some imports not used depending on template conditions
// @ts-ignore
import { DUMMY_BASE_URL, assertParamExists, setApiKeyToObject, setBasicAuthToObject, setBearerAuthToObject, setOAuthToObject, setSearchParams, serializeDataIfNeeded, toPathString, createRequestFunction } from './common';
import type { RequestArgs } from './base';
// @ts-ignore
import { BASE_PATH, COLLECTION_FORMATS, BaseAPI, RequiredError, operationServerMap } from './base';

/**
 * 
 * @export
 * @interface HTTPValidationError
 */
export interface HTTPValidationError {
    /**
     * 
     * @type {Array<ValidationError>}
     * @memberof HTTPValidationError
     */
    'detail'?: Array<ValidationError>;
}
/**
 * 
 * @export
 * @interface LocationInner
 */
export interface LocationInner {
}
/**
 * 
 * @export
 * @interface User
 */
export interface User {
    /**
     * 
     * @type {string}
     * @memberof User
     */
    'username': string;
    /**
     * 
     * @type {string}
     * @memberof User
     */
    'first_name': string;
    /**
     * 
     * @type {string}
     * @memberof User
     */
    'last_name': string;
    /**
     * 
     * @type {string}
     * @memberof User
     */
    'email'?: string;
    /**
     * 
     * @type {string}
     * @memberof User
     */
    'access_token': string;
    /**
     * 
     * @type {string}
     * @memberof User
     */
    'token_type': string;
    /**
     * 
     * @type {number}
     * @memberof User
     */
    'last_activity_unixtime'?: number;
}
/**
 * 
 * @export
 * @interface ValidationError
 */
export interface ValidationError {
    /**
     * 
     * @type {Array<LocationInner>}
     * @memberof ValidationError
     */
    'loc': Array<LocationInner>;
    /**
     * 
     * @type {string}
     * @memberof ValidationError
     */
    'msg': string;
    /**
     * 
     * @type {string}
     * @memberof ValidationError
     */
    'type': string;
}

/**
 * HealthApi - axios parameter creator
 * @export
 */
export const HealthApiAxiosParamCreator = function (configuration?: Configuration) {
    return {
        /**
         * Readiness health endpoint.  Returns -------     Status dictionary  Raises ------ HTTPException     500: User table does not exist
         * @summary Readiness
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        readinessApiV1UserloginHealthReadinessGet: async (options: RawAxiosRequestConfig = {}): Promise<RequestArgs> => {
            const localVarPath = `/api/v1/userlogin/health/readiness`;
            // use dummy base URL string because the URL constructor only accepts absolute URLs.
            const localVarUrlObj = new URL(localVarPath, DUMMY_BASE_URL);
            let baseOptions;
            if (configuration) {
                baseOptions = configuration.baseOptions;
            }

            const localVarRequestOptions = { method: 'GET', ...baseOptions, ...options};
            const localVarHeaderParameter = {} as any;
            const localVarQueryParameter = {} as any;


    
            setSearchParams(localVarUrlObj, localVarQueryParameter);
            let headersFromBaseOptions = baseOptions && baseOptions.headers ? baseOptions.headers : {};
            localVarRequestOptions.headers = {...localVarHeaderParameter, ...headersFromBaseOptions, ...options.headers};

            return {
                url: toPathString(localVarUrlObj),
                options: localVarRequestOptions,
            };
        },
    }
};

/**
 * HealthApi - functional programming interface
 * @export
 */
export const HealthApiFp = function(configuration?: Configuration) {
    const localVarAxiosParamCreator = HealthApiAxiosParamCreator(configuration)
    return {
        /**
         * Readiness health endpoint.  Returns -------     Status dictionary  Raises ------ HTTPException     500: User table does not exist
         * @summary Readiness
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        async readinessApiV1UserloginHealthReadinessGet(options?: RawAxiosRequestConfig): Promise<(axios?: AxiosInstance, basePath?: string) => AxiosPromise<any>> {
            const localVarAxiosArgs = await localVarAxiosParamCreator.readinessApiV1UserloginHealthReadinessGet(options);
            const localVarOperationServerIndex = configuration?.serverIndex ?? 0;
            const localVarOperationServerBasePath = operationServerMap['HealthApi.readinessApiV1UserloginHealthReadinessGet']?.[localVarOperationServerIndex]?.url;
            return (axios, basePath) => createRequestFunction(localVarAxiosArgs, globalAxios, BASE_PATH, configuration)(axios, localVarOperationServerBasePath || basePath);
        },
    }
};

/**
 * HealthApi - factory interface
 * @export
 */
export const HealthApiFactory = function (configuration?: Configuration, basePath?: string, axios?: AxiosInstance) {
    const localVarFp = HealthApiFp(configuration)
    return {
        /**
         * Readiness health endpoint.  Returns -------     Status dictionary  Raises ------ HTTPException     500: User table does not exist
         * @summary Readiness
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        readinessApiV1UserloginHealthReadinessGet(options?: any): AxiosPromise<any> {
            return localVarFp.readinessApiV1UserloginHealthReadinessGet(options).then((request) => request(axios, basePath));
        },
    };
};

/**
 * HealthApi - object-oriented interface
 * @export
 * @class HealthApi
 * @extends {BaseAPI}
 */
export class HealthApi extends BaseAPI {
    /**
     * Readiness health endpoint.  Returns -------     Status dictionary  Raises ------ HTTPException     500: User table does not exist
     * @summary Readiness
     * @param {*} [options] Override http request option.
     * @throws {RequiredError}
     * @memberof HealthApi
     */
    public readinessApiV1UserloginHealthReadinessGet(options?: RawAxiosRequestConfig) {
        return HealthApiFp(this.configuration).readinessApiV1UserloginHealthReadinessGet(options).then((request) => request(this.axios, this.basePath));
    }
}



/**
 * LoginApi - axios parameter creator
 * @export
 */
export const LoginApiAxiosParamCreator = function (configuration?: Configuration) {
    return {
        /**
         * Login endpoint.  Parameters ---------- form_data     Http form data for OAuth2 compliant login with username and password.  Returns -------     User pydantic model, the user data in case of a successful login.  Raises ------ HTTPException     401: Unauthorized if the username or password is wrong.
         * @summary Login
         * @param {string} username 
         * @param {string} password 
         * @param {string} [grantType] 
         * @param {string} [scope] 
         * @param {string} [clientId] 
         * @param {string} [clientSecret] 
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        loginApiV1UserloginLoginPost: async (username: string, password: string, grantType?: string, scope?: string, clientId?: string, clientSecret?: string, options: RawAxiosRequestConfig = {}): Promise<RequestArgs> => {
            // verify required parameter 'username' is not null or undefined
            assertParamExists('loginApiV1UserloginLoginPost', 'username', username)
            // verify required parameter 'password' is not null or undefined
            assertParamExists('loginApiV1UserloginLoginPost', 'password', password)
            const localVarPath = `/api/v1/userlogin/login`;
            // use dummy base URL string because the URL constructor only accepts absolute URLs.
            const localVarUrlObj = new URL(localVarPath, DUMMY_BASE_URL);
            let baseOptions;
            if (configuration) {
                baseOptions = configuration.baseOptions;
            }

            const localVarRequestOptions = { method: 'POST', ...baseOptions, ...options};
            const localVarHeaderParameter = {} as any;
            const localVarQueryParameter = {} as any;
            const localVarFormParams = new URLSearchParams();


            if (grantType !== undefined) { 
                localVarFormParams.set('grant_type', grantType as any);
            }
    
            if (username !== undefined) { 
                localVarFormParams.set('username', username as any);
            }
    
            if (password !== undefined) { 
                localVarFormParams.set('password', password as any);
            }
    
            if (scope !== undefined) { 
                localVarFormParams.set('scope', scope as any);
            }
    
            if (clientId !== undefined) { 
                localVarFormParams.set('client_id', clientId as any);
            }
    
            if (clientSecret !== undefined) { 
                localVarFormParams.set('client_secret', clientSecret as any);
            }
    
    
            localVarHeaderParameter['Content-Type'] = 'application/x-www-form-urlencoded';
    
            setSearchParams(localVarUrlObj, localVarQueryParameter);
            let headersFromBaseOptions = baseOptions && baseOptions.headers ? baseOptions.headers : {};
            localVarRequestOptions.headers = {...localVarHeaderParameter, ...headersFromBaseOptions, ...options.headers};
            localVarRequestOptions.data = localVarFormParams.toString();

            return {
                url: toPathString(localVarUrlObj),
                options: localVarRequestOptions,
            };
        },
        /**
         * Logout endpoint.
         * @summary Login
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        loginApiV1UserloginLogoutPost: async (options: RawAxiosRequestConfig = {}): Promise<RequestArgs> => {
            const localVarPath = `/api/v1/userlogin/logout`;
            // use dummy base URL string because the URL constructor only accepts absolute URLs.
            const localVarUrlObj = new URL(localVarPath, DUMMY_BASE_URL);
            let baseOptions;
            if (configuration) {
                baseOptions = configuration.baseOptions;
            }

            const localVarRequestOptions = { method: 'POST', ...baseOptions, ...options};
            const localVarHeaderParameter = {} as any;
            const localVarQueryParameter = {} as any;

            // authentication OAuth2PasswordBearer required
            // oauth required
            await setOAuthToObject(localVarHeaderParameter, "OAuth2PasswordBearer", [], configuration)


    
            setSearchParams(localVarUrlObj, localVarQueryParameter);
            let headersFromBaseOptions = baseOptions && baseOptions.headers ? baseOptions.headers : {};
            localVarRequestOptions.headers = {...localVarHeaderParameter, ...headersFromBaseOptions, ...options.headers};

            return {
                url: toPathString(localVarUrlObj),
                options: localVarRequestOptions,
            };
        },
    }
};

/**
 * LoginApi - functional programming interface
 * @export
 */
export const LoginApiFp = function(configuration?: Configuration) {
    const localVarAxiosParamCreator = LoginApiAxiosParamCreator(configuration)
    return {
        /**
         * Login endpoint.  Parameters ---------- form_data     Http form data for OAuth2 compliant login with username and password.  Returns -------     User pydantic model, the user data in case of a successful login.  Raises ------ HTTPException     401: Unauthorized if the username or password is wrong.
         * @summary Login
         * @param {string} username 
         * @param {string} password 
         * @param {string} [grantType] 
         * @param {string} [scope] 
         * @param {string} [clientId] 
         * @param {string} [clientSecret] 
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        async loginApiV1UserloginLoginPost(username: string, password: string, grantType?: string, scope?: string, clientId?: string, clientSecret?: string, options?: RawAxiosRequestConfig): Promise<(axios?: AxiosInstance, basePath?: string) => AxiosPromise<User>> {
            const localVarAxiosArgs = await localVarAxiosParamCreator.loginApiV1UserloginLoginPost(username, password, grantType, scope, clientId, clientSecret, options);
            const localVarOperationServerIndex = configuration?.serverIndex ?? 0;
            const localVarOperationServerBasePath = operationServerMap['LoginApi.loginApiV1UserloginLoginPost']?.[localVarOperationServerIndex]?.url;
            return (axios, basePath) => createRequestFunction(localVarAxiosArgs, globalAxios, BASE_PATH, configuration)(axios, localVarOperationServerBasePath || basePath);
        },
        /**
         * Logout endpoint.
         * @summary Login
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        async loginApiV1UserloginLogoutPost(options?: RawAxiosRequestConfig): Promise<(axios?: AxiosInstance, basePath?: string) => AxiosPromise<any>> {
            const localVarAxiosArgs = await localVarAxiosParamCreator.loginApiV1UserloginLogoutPost(options);
            const localVarOperationServerIndex = configuration?.serverIndex ?? 0;
            const localVarOperationServerBasePath = operationServerMap['LoginApi.loginApiV1UserloginLogoutPost']?.[localVarOperationServerIndex]?.url;
            return (axios, basePath) => createRequestFunction(localVarAxiosArgs, globalAxios, BASE_PATH, configuration)(axios, localVarOperationServerBasePath || basePath);
        },
    }
};

/**
 * LoginApi - factory interface
 * @export
 */
export const LoginApiFactory = function (configuration?: Configuration, basePath?: string, axios?: AxiosInstance) {
    const localVarFp = LoginApiFp(configuration)
    return {
        /**
         * Login endpoint.  Parameters ---------- form_data     Http form data for OAuth2 compliant login with username and password.  Returns -------     User pydantic model, the user data in case of a successful login.  Raises ------ HTTPException     401: Unauthorized if the username or password is wrong.
         * @summary Login
         * @param {string} username 
         * @param {string} password 
         * @param {string} [grantType] 
         * @param {string} [scope] 
         * @param {string} [clientId] 
         * @param {string} [clientSecret] 
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        loginApiV1UserloginLoginPost(username: string, password: string, grantType?: string, scope?: string, clientId?: string, clientSecret?: string, options?: any): AxiosPromise<User> {
            return localVarFp.loginApiV1UserloginLoginPost(username, password, grantType, scope, clientId, clientSecret, options).then((request) => request(axios, basePath));
        },
        /**
         * Logout endpoint.
         * @summary Login
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        loginApiV1UserloginLogoutPost(options?: any): AxiosPromise<any> {
            return localVarFp.loginApiV1UserloginLogoutPost(options).then((request) => request(axios, basePath));
        },
    };
};

/**
 * LoginApi - object-oriented interface
 * @export
 * @class LoginApi
 * @extends {BaseAPI}
 */
export class LoginApi extends BaseAPI {
    /**
     * Login endpoint.  Parameters ---------- form_data     Http form data for OAuth2 compliant login with username and password.  Returns -------     User pydantic model, the user data in case of a successful login.  Raises ------ HTTPException     401: Unauthorized if the username or password is wrong.
     * @summary Login
     * @param {string} username 
     * @param {string} password 
     * @param {string} [grantType] 
     * @param {string} [scope] 
     * @param {string} [clientId] 
     * @param {string} [clientSecret] 
     * @param {*} [options] Override http request option.
     * @throws {RequiredError}
     * @memberof LoginApi
     */
    public loginApiV1UserloginLoginPost(username: string, password: string, grantType?: string, scope?: string, clientId?: string, clientSecret?: string, options?: RawAxiosRequestConfig) {
        return LoginApiFp(this.configuration).loginApiV1UserloginLoginPost(username, password, grantType, scope, clientId, clientSecret, options).then((request) => request(this.axios, this.basePath));
    }

    /**
     * Logout endpoint.
     * @summary Login
     * @param {*} [options] Override http request option.
     * @throws {RequiredError}
     * @memberof LoginApi
     */
    public loginApiV1UserloginLogoutPost(options?: RawAxiosRequestConfig) {
        return LoginApiFp(this.configuration).loginApiV1UserloginLogoutPost(options).then((request) => request(this.axios, this.basePath));
    }
}



/**
 * UserApi - axios parameter creator
 * @export
 */
export const UserApiAxiosParamCreator = function (configuration?: Configuration) {
    return {
        /**
         * Create new patient database entry.  Parameters ---------- new_user     pydantic base model of new user, token_type should be \"password\" and access_token should contain the password of the new user.     The password of the new user should at least be 12 characters long.  Returns -------     Patient pydantic output model
         * @summary Create User
         * @param {User} user 
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        createUserApiV1UserloginCreateuserPost: async (user: User, options: RawAxiosRequestConfig = {}): Promise<RequestArgs> => {
            // verify required parameter 'user' is not null or undefined
            assertParamExists('createUserApiV1UserloginCreateuserPost', 'user', user)
            const localVarPath = `/api/v1/userlogin/createuser`;
            // use dummy base URL string because the URL constructor only accepts absolute URLs.
            const localVarUrlObj = new URL(localVarPath, DUMMY_BASE_URL);
            let baseOptions;
            if (configuration) {
                baseOptions = configuration.baseOptions;
            }

            const localVarRequestOptions = { method: 'POST', ...baseOptions, ...options};
            const localVarHeaderParameter = {} as any;
            const localVarQueryParameter = {} as any;

            // authentication OAuth2PasswordBearer required
            // oauth required
            await setOAuthToObject(localVarHeaderParameter, "OAuth2PasswordBearer", [], configuration)


    
            localVarHeaderParameter['Content-Type'] = 'application/json';

            setSearchParams(localVarUrlObj, localVarQueryParameter);
            let headersFromBaseOptions = baseOptions && baseOptions.headers ? baseOptions.headers : {};
            localVarRequestOptions.headers = {...localVarHeaderParameter, ...headersFromBaseOptions, ...options.headers};
            localVarRequestOptions.data = serializeDataIfNeeded(user, localVarRequestOptions, configuration)

            return {
                url: toPathString(localVarUrlObj),
                options: localVarRequestOptions,
            };
        },
        /**
         * Get current user endpoint.  Parameters ---------- access_token      User token (HTTP Header: \"Authorization: Bearer <access_token>\")  Returns -------     User pydantic model, the user data of the current user.  Raises ------ HTTPException     401: Unauthorized if the token is invalid.
         * @summary Get Current User
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        getCurrentUserApiV1UserloginGetcurrentuserGet: async (options: RawAxiosRequestConfig = {}): Promise<RequestArgs> => {
            const localVarPath = `/api/v1/userlogin/getcurrentuser`;
            // use dummy base URL string because the URL constructor only accepts absolute URLs.
            const localVarUrlObj = new URL(localVarPath, DUMMY_BASE_URL);
            let baseOptions;
            if (configuration) {
                baseOptions = configuration.baseOptions;
            }

            const localVarRequestOptions = { method: 'GET', ...baseOptions, ...options};
            const localVarHeaderParameter = {} as any;
            const localVarQueryParameter = {} as any;

            // authentication OAuth2PasswordBearer required
            // oauth required
            await setOAuthToObject(localVarHeaderParameter, "OAuth2PasswordBearer", [], configuration)


    
            setSearchParams(localVarUrlObj, localVarQueryParameter);
            let headersFromBaseOptions = baseOptions && baseOptions.headers ? baseOptions.headers : {};
            localVarRequestOptions.headers = {...localVarHeaderParameter, ...headersFromBaseOptions, ...options.headers};

            return {
                url: toPathString(localVarUrlObj),
                options: localVarRequestOptions,
            };
        },
        /**
         * Get all users endpoint.  Returns -------     List of all users. The access_token and token_type properties are set to \"\" for all of them.
         * @summary Get User List
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        getUserListApiV1UserloginGetallusersGet: async (options: RawAxiosRequestConfig = {}): Promise<RequestArgs> => {
            const localVarPath = `/api/v1/userlogin/getallusers`;
            // use dummy base URL string because the URL constructor only accepts absolute URLs.
            const localVarUrlObj = new URL(localVarPath, DUMMY_BASE_URL);
            let baseOptions;
            if (configuration) {
                baseOptions = configuration.baseOptions;
            }

            const localVarRequestOptions = { method: 'GET', ...baseOptions, ...options};
            const localVarHeaderParameter = {} as any;
            const localVarQueryParameter = {} as any;

            // authentication OAuth2PasswordBearer required
            // oauth required
            await setOAuthToObject(localVarHeaderParameter, "OAuth2PasswordBearer", [], configuration)


    
            setSearchParams(localVarUrlObj, localVarQueryParameter);
            let headersFromBaseOptions = baseOptions && baseOptions.headers ? baseOptions.headers : {};
            localVarRequestOptions.headers = {...localVarHeaderParameter, ...headersFromBaseOptions, ...options.headers};

            return {
                url: toPathString(localVarUrlObj),
                options: localVarRequestOptions,
            };
        },
        /**
         * Delete an existing user.  Parameters ---------- user_to_delete     User to delete.  Raises ------ HTTPException     404: Not found
         * @summary User Delete
         * @param {string} usernameToDelete 
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        userDeleteApiV1UserloginDeleteuserDelete: async (usernameToDelete: string, options: RawAxiosRequestConfig = {}): Promise<RequestArgs> => {
            // verify required parameter 'usernameToDelete' is not null or undefined
            assertParamExists('userDeleteApiV1UserloginDeleteuserDelete', 'usernameToDelete', usernameToDelete)
            const localVarPath = `/api/v1/userlogin/deleteuser`;
            // use dummy base URL string because the URL constructor only accepts absolute URLs.
            const localVarUrlObj = new URL(localVarPath, DUMMY_BASE_URL);
            let baseOptions;
            if (configuration) {
                baseOptions = configuration.baseOptions;
            }

            const localVarRequestOptions = { method: 'DELETE', ...baseOptions, ...options};
            const localVarHeaderParameter = {} as any;
            const localVarQueryParameter = {} as any;

            // authentication OAuth2PasswordBearer required
            // oauth required
            await setOAuthToObject(localVarHeaderParameter, "OAuth2PasswordBearer", [], configuration)

            if (usernameToDelete !== undefined) {
                localVarQueryParameter['username_to_delete'] = usernameToDelete;
            }


    
            setSearchParams(localVarUrlObj, localVarQueryParameter);
            let headersFromBaseOptions = baseOptions && baseOptions.headers ? baseOptions.headers : {};
            localVarRequestOptions.headers = {...localVarHeaderParameter, ...headersFromBaseOptions, ...options.headers};

            return {
                url: toPathString(localVarUrlObj),
                options: localVarRequestOptions,
            };
        },
    }
};

/**
 * UserApi - functional programming interface
 * @export
 */
export const UserApiFp = function(configuration?: Configuration) {
    const localVarAxiosParamCreator = UserApiAxiosParamCreator(configuration)
    return {
        /**
         * Create new patient database entry.  Parameters ---------- new_user     pydantic base model of new user, token_type should be \"password\" and access_token should contain the password of the new user.     The password of the new user should at least be 12 characters long.  Returns -------     Patient pydantic output model
         * @summary Create User
         * @param {User} user 
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        async createUserApiV1UserloginCreateuserPost(user: User, options?: RawAxiosRequestConfig): Promise<(axios?: AxiosInstance, basePath?: string) => AxiosPromise<any>> {
            const localVarAxiosArgs = await localVarAxiosParamCreator.createUserApiV1UserloginCreateuserPost(user, options);
            const localVarOperationServerIndex = configuration?.serverIndex ?? 0;
            const localVarOperationServerBasePath = operationServerMap['UserApi.createUserApiV1UserloginCreateuserPost']?.[localVarOperationServerIndex]?.url;
            return (axios, basePath) => createRequestFunction(localVarAxiosArgs, globalAxios, BASE_PATH, configuration)(axios, localVarOperationServerBasePath || basePath);
        },
        /**
         * Get current user endpoint.  Parameters ---------- access_token      User token (HTTP Header: \"Authorization: Bearer <access_token>\")  Returns -------     User pydantic model, the user data of the current user.  Raises ------ HTTPException     401: Unauthorized if the token is invalid.
         * @summary Get Current User
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        async getCurrentUserApiV1UserloginGetcurrentuserGet(options?: RawAxiosRequestConfig): Promise<(axios?: AxiosInstance, basePath?: string) => AxiosPromise<User>> {
            const localVarAxiosArgs = await localVarAxiosParamCreator.getCurrentUserApiV1UserloginGetcurrentuserGet(options);
            const localVarOperationServerIndex = configuration?.serverIndex ?? 0;
            const localVarOperationServerBasePath = operationServerMap['UserApi.getCurrentUserApiV1UserloginGetcurrentuserGet']?.[localVarOperationServerIndex]?.url;
            return (axios, basePath) => createRequestFunction(localVarAxiosArgs, globalAxios, BASE_PATH, configuration)(axios, localVarOperationServerBasePath || basePath);
        },
        /**
         * Get all users endpoint.  Returns -------     List of all users. The access_token and token_type properties are set to \"\" for all of them.
         * @summary Get User List
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        async getUserListApiV1UserloginGetallusersGet(options?: RawAxiosRequestConfig): Promise<(axios?: AxiosInstance, basePath?: string) => AxiosPromise<Array<User>>> {
            const localVarAxiosArgs = await localVarAxiosParamCreator.getUserListApiV1UserloginGetallusersGet(options);
            const localVarOperationServerIndex = configuration?.serverIndex ?? 0;
            const localVarOperationServerBasePath = operationServerMap['UserApi.getUserListApiV1UserloginGetallusersGet']?.[localVarOperationServerIndex]?.url;
            return (axios, basePath) => createRequestFunction(localVarAxiosArgs, globalAxios, BASE_PATH, configuration)(axios, localVarOperationServerBasePath || basePath);
        },
        /**
         * Delete an existing user.  Parameters ---------- user_to_delete     User to delete.  Raises ------ HTTPException     404: Not found
         * @summary User Delete
         * @param {string} usernameToDelete 
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        async userDeleteApiV1UserloginDeleteuserDelete(usernameToDelete: string, options?: RawAxiosRequestConfig): Promise<(axios?: AxiosInstance, basePath?: string) => AxiosPromise<void>> {
            const localVarAxiosArgs = await localVarAxiosParamCreator.userDeleteApiV1UserloginDeleteuserDelete(usernameToDelete, options);
            const localVarOperationServerIndex = configuration?.serverIndex ?? 0;
            const localVarOperationServerBasePath = operationServerMap['UserApi.userDeleteApiV1UserloginDeleteuserDelete']?.[localVarOperationServerIndex]?.url;
            return (axios, basePath) => createRequestFunction(localVarAxiosArgs, globalAxios, BASE_PATH, configuration)(axios, localVarOperationServerBasePath || basePath);
        },
    }
};

/**
 * UserApi - factory interface
 * @export
 */
export const UserApiFactory = function (configuration?: Configuration, basePath?: string, axios?: AxiosInstance) {
    const localVarFp = UserApiFp(configuration)
    return {
        /**
         * Create new patient database entry.  Parameters ---------- new_user     pydantic base model of new user, token_type should be \"password\" and access_token should contain the password of the new user.     The password of the new user should at least be 12 characters long.  Returns -------     Patient pydantic output model
         * @summary Create User
         * @param {User} user 
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        createUserApiV1UserloginCreateuserPost(user: User, options?: any): AxiosPromise<any> {
            return localVarFp.createUserApiV1UserloginCreateuserPost(user, options).then((request) => request(axios, basePath));
        },
        /**
         * Get current user endpoint.  Parameters ---------- access_token      User token (HTTP Header: \"Authorization: Bearer <access_token>\")  Returns -------     User pydantic model, the user data of the current user.  Raises ------ HTTPException     401: Unauthorized if the token is invalid.
         * @summary Get Current User
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        getCurrentUserApiV1UserloginGetcurrentuserGet(options?: any): AxiosPromise<User> {
            return localVarFp.getCurrentUserApiV1UserloginGetcurrentuserGet(options).then((request) => request(axios, basePath));
        },
        /**
         * Get all users endpoint.  Returns -------     List of all users. The access_token and token_type properties are set to \"\" for all of them.
         * @summary Get User List
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        getUserListApiV1UserloginGetallusersGet(options?: any): AxiosPromise<Array<User>> {
            return localVarFp.getUserListApiV1UserloginGetallusersGet(options).then((request) => request(axios, basePath));
        },
        /**
         * Delete an existing user.  Parameters ---------- user_to_delete     User to delete.  Raises ------ HTTPException     404: Not found
         * @summary User Delete
         * @param {string} usernameToDelete 
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        userDeleteApiV1UserloginDeleteuserDelete(usernameToDelete: string, options?: any): AxiosPromise<void> {
            return localVarFp.userDeleteApiV1UserloginDeleteuserDelete(usernameToDelete, options).then((request) => request(axios, basePath));
        },
    };
};

/**
 * UserApi - object-oriented interface
 * @export
 * @class UserApi
 * @extends {BaseAPI}
 */
export class UserApi extends BaseAPI {
    /**
     * Create new patient database entry.  Parameters ---------- new_user     pydantic base model of new user, token_type should be \"password\" and access_token should contain the password of the new user.     The password of the new user should at least be 12 characters long.  Returns -------     Patient pydantic output model
     * @summary Create User
     * @param {User} user 
     * @param {*} [options] Override http request option.
     * @throws {RequiredError}
     * @memberof UserApi
     */
    public createUserApiV1UserloginCreateuserPost(user: User, options?: RawAxiosRequestConfig) {
        return UserApiFp(this.configuration).createUserApiV1UserloginCreateuserPost(user, options).then((request) => request(this.axios, this.basePath));
    }

    /**
     * Get current user endpoint.  Parameters ---------- access_token      User token (HTTP Header: \"Authorization: Bearer <access_token>\")  Returns -------     User pydantic model, the user data of the current user.  Raises ------ HTTPException     401: Unauthorized if the token is invalid.
     * @summary Get Current User
     * @param {*} [options] Override http request option.
     * @throws {RequiredError}
     * @memberof UserApi
     */
    public getCurrentUserApiV1UserloginGetcurrentuserGet(options?: RawAxiosRequestConfig) {
        return UserApiFp(this.configuration).getCurrentUserApiV1UserloginGetcurrentuserGet(options).then((request) => request(this.axios, this.basePath));
    }

    /**
     * Get all users endpoint.  Returns -------     List of all users. The access_token and token_type properties are set to \"\" for all of them.
     * @summary Get User List
     * @param {*} [options] Override http request option.
     * @throws {RequiredError}
     * @memberof UserApi
     */
    public getUserListApiV1UserloginGetallusersGet(options?: RawAxiosRequestConfig) {
        return UserApiFp(this.configuration).getUserListApiV1UserloginGetallusersGet(options).then((request) => request(this.axios, this.basePath));
    }

    /**
     * Delete an existing user.  Parameters ---------- user_to_delete     User to delete.  Raises ------ HTTPException     404: Not found
     * @summary User Delete
     * @param {string} usernameToDelete 
     * @param {*} [options] Override http request option.
     * @throws {RequiredError}
     * @memberof UserApi
     */
    public userDeleteApiV1UserloginDeleteuserDelete(usernameToDelete: string, options?: RawAxiosRequestConfig) {
        return UserApiFp(this.configuration).userDeleteApiV1UserloginDeleteuserDelete(usernameToDelete, options).then((request) => request(this.axios, this.basePath));
    }
}



