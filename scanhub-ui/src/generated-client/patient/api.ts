/* tslint:disable */
/* eslint-disable */
/**
 * ScanHub-UI
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
 * Patient pydantic base model.
 * @export
 * @interface BasePatient
 */
export interface BasePatient {
    /**
     * 
     * @type {string}
     * @memberof BasePatient
     */
    'first_name': string;
    /**
     * 
     * @type {string}
     * @memberof BasePatient
     */
    'last_name': string;
    /**
     * 
     * @type {string}
     * @memberof BasePatient
     */
    'birth_date': string;
    /**
     * 
     * @type {Gender}
     * @memberof BasePatient
     */
    'sex': Gender;
    /**
     * 
     * @type {string}
     * @memberof BasePatient
     */
    'issuer': string;
    /**
     * 
     * @type {string}
     * @memberof BasePatient
     */
    'status': BasePatientStatusEnum;
    /**
     * 
     * @type {string}
     * @memberof BasePatient
     */
    'comment'?: string;
}

export const BasePatientStatusEnum = {
    New: 'NEW',
    Updated: 'UPDATED',
    Deleted: 'DELETED'
} as const;

export type BasePatientStatusEnum = typeof BasePatientStatusEnum[keyof typeof BasePatientStatusEnum];

/**
 * Pydantic definition of genders.
 * @export
 * @enum {string}
 */

export const Gender = {
    Male: 'MALE',
    Female: 'FEMALE',
    Other: 'OTHER',
    NotGiven: 'NOT_GIVEN'
} as const;

export type Gender = typeof Gender[keyof typeof Gender];


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
 * Patient pydantic output model.
 * @export
 * @interface PatientOut
 */
export interface PatientOut {
    /**
     * 
     * @type {string}
     * @memberof PatientOut
     */
    'first_name': string;
    /**
     * 
     * @type {string}
     * @memberof PatientOut
     */
    'last_name': string;
    /**
     * 
     * @type {string}
     * @memberof PatientOut
     */
    'birth_date': string;
    /**
     * 
     * @type {Gender}
     * @memberof PatientOut
     */
    'sex': Gender;
    /**
     * 
     * @type {string}
     * @memberof PatientOut
     */
    'issuer': string;
    /**
     * 
     * @type {string}
     * @memberof PatientOut
     */
    'status': PatientOutStatusEnum;
    /**
     * 
     * @type {string}
     * @memberof PatientOut
     */
    'comment'?: string;
    /**
     * 
     * @type {number}
     * @memberof PatientOut
     */
    'id': number;
    /**
     * 
     * @type {string}
     * @memberof PatientOut
     */
    'datetime_created': string;
    /**
     * 
     * @type {string}
     * @memberof PatientOut
     */
    'datetime_updated'?: string;
}

export const PatientOutStatusEnum = {
    New: 'NEW',
    Updated: 'UPDATED',
    Deleted: 'DELETED'
} as const;

export type PatientOutStatusEnum = typeof PatientOutStatusEnum[keyof typeof PatientOutStatusEnum];

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
 * PatientsApi - axios parameter creator
 * @export
 */
export const PatientsApiAxiosParamCreator = function (configuration?: Configuration) {
    return {
        /**
         * Create new patient database entry.  Parameters ---------- payload     Patient pydantic base model  Returns -------     Patient pydantic output model  Raises ------ HTTPException     404: Could not create patient
         * @summary Create Patient
         * @param {BasePatient} basePatient 
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        createPatientApiV1PatientPost: async (basePatient: BasePatient, options: RawAxiosRequestConfig = {}): Promise<RequestArgs> => {
            // verify required parameter 'basePatient' is not null or undefined
            assertParamExists('createPatientApiV1PatientPost', 'basePatient', basePatient)
            const localVarPath = `/api/v1/patient/`;
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
            localVarRequestOptions.data = serializeDataIfNeeded(basePatient, localVarRequestOptions, configuration)

            return {
                url: toPathString(localVarUrlObj),
                options: localVarRequestOptions,
            };
        },
        /**
         * Delete patient from database.  Parameters ---------- patient_id     Id of patient to be deleted  Raises ------ HTTPException     _description_
         * @summary Delete Patient
         * @param {number} patientId 
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        deletePatientApiV1PatientPatientIdDelete: async (patientId: number, options: RawAxiosRequestConfig = {}): Promise<RequestArgs> => {
            // verify required parameter 'patientId' is not null or undefined
            assertParamExists('deletePatientApiV1PatientPatientIdDelete', 'patientId', patientId)
            const localVarPath = `/api/v1/patient/{patient_id}`
                .replace(`{${"patient_id"}}`, encodeURIComponent(String(patientId)));
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


    
            setSearchParams(localVarUrlObj, localVarQueryParameter);
            let headersFromBaseOptions = baseOptions && baseOptions.headers ? baseOptions.headers : {};
            localVarRequestOptions.headers = {...localVarHeaderParameter, ...headersFromBaseOptions, ...options.headers};

            return {
                url: toPathString(localVarUrlObj),
                options: localVarRequestOptions,
            };
        },
        /**
         * Get a patient from database by id.  Parameters ---------- patient_id     Id of the requested patient  Returns -------     Patient pydantic output model  Raises ------ HTTPException     404: Patient not found
         * @summary Get Patient
         * @param {number} patientId 
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        getPatientApiV1PatientPatientIdGet: async (patientId: number, options: RawAxiosRequestConfig = {}): Promise<RequestArgs> => {
            // verify required parameter 'patientId' is not null or undefined
            assertParamExists('getPatientApiV1PatientPatientIdGet', 'patientId', patientId)
            const localVarPath = `/api/v1/patient/{patient_id}`
                .replace(`{${"patient_id"}}`, encodeURIComponent(String(patientId)));
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
         * Get all patients endpoint.  Returns -------     List of patient pydantic output models
         * @summary Get Patient List
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        getPatientListApiV1PatientGet: async (options: RawAxiosRequestConfig = {}): Promise<RequestArgs> => {
            const localVarPath = `/api/v1/patient/`;
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
         * Update existing patient endpoint.  Parameters ---------- patient_id     Id of the patient to be updated payload     Patient data to be updated  Returns -------     Updated patient pydantic output model  Raises ------ HTTPException     404: Patient not found
         * @summary Update Patient
         * @param {number} patientId 
         * @param {BasePatient} basePatient 
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        updatePatientApiV1PatientPatientIdPut: async (patientId: number, basePatient: BasePatient, options: RawAxiosRequestConfig = {}): Promise<RequestArgs> => {
            // verify required parameter 'patientId' is not null or undefined
            assertParamExists('updatePatientApiV1PatientPatientIdPut', 'patientId', patientId)
            // verify required parameter 'basePatient' is not null or undefined
            assertParamExists('updatePatientApiV1PatientPatientIdPut', 'basePatient', basePatient)
            const localVarPath = `/api/v1/patient/{patient_id}`
                .replace(`{${"patient_id"}}`, encodeURIComponent(String(patientId)));
            // use dummy base URL string because the URL constructor only accepts absolute URLs.
            const localVarUrlObj = new URL(localVarPath, DUMMY_BASE_URL);
            let baseOptions;
            if (configuration) {
                baseOptions = configuration.baseOptions;
            }

            const localVarRequestOptions = { method: 'PUT', ...baseOptions, ...options};
            const localVarHeaderParameter = {} as any;
            const localVarQueryParameter = {} as any;

            // authentication OAuth2PasswordBearer required
            // oauth required
            await setOAuthToObject(localVarHeaderParameter, "OAuth2PasswordBearer", [], configuration)


    
            localVarHeaderParameter['Content-Type'] = 'application/json';

            setSearchParams(localVarUrlObj, localVarQueryParameter);
            let headersFromBaseOptions = baseOptions && baseOptions.headers ? baseOptions.headers : {};
            localVarRequestOptions.headers = {...localVarHeaderParameter, ...headersFromBaseOptions, ...options.headers};
            localVarRequestOptions.data = serializeDataIfNeeded(basePatient, localVarRequestOptions, configuration)

            return {
                url: toPathString(localVarUrlObj),
                options: localVarRequestOptions,
            };
        },
    }
};

/**
 * PatientsApi - functional programming interface
 * @export
 */
export const PatientsApiFp = function(configuration?: Configuration) {
    const localVarAxiosParamCreator = PatientsApiAxiosParamCreator(configuration)
    return {
        /**
         * Create new patient database entry.  Parameters ---------- payload     Patient pydantic base model  Returns -------     Patient pydantic output model  Raises ------ HTTPException     404: Could not create patient
         * @summary Create Patient
         * @param {BasePatient} basePatient 
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        async createPatientApiV1PatientPost(basePatient: BasePatient, options?: RawAxiosRequestConfig): Promise<(axios?: AxiosInstance, basePath?: string) => AxiosPromise<PatientOut>> {
            const localVarAxiosArgs = await localVarAxiosParamCreator.createPatientApiV1PatientPost(basePatient, options);
            const localVarOperationServerIndex = configuration?.serverIndex ?? 0;
            const localVarOperationServerBasePath = operationServerMap['PatientsApi.createPatientApiV1PatientPost']?.[localVarOperationServerIndex]?.url;
            return (axios, basePath) => createRequestFunction(localVarAxiosArgs, globalAxios, BASE_PATH, configuration)(axios, localVarOperationServerBasePath || basePath);
        },
        /**
         * Delete patient from database.  Parameters ---------- patient_id     Id of patient to be deleted  Raises ------ HTTPException     _description_
         * @summary Delete Patient
         * @param {number} patientId 
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        async deletePatientApiV1PatientPatientIdDelete(patientId: number, options?: RawAxiosRequestConfig): Promise<(axios?: AxiosInstance, basePath?: string) => AxiosPromise<void>> {
            const localVarAxiosArgs = await localVarAxiosParamCreator.deletePatientApiV1PatientPatientIdDelete(patientId, options);
            const localVarOperationServerIndex = configuration?.serverIndex ?? 0;
            const localVarOperationServerBasePath = operationServerMap['PatientsApi.deletePatientApiV1PatientPatientIdDelete']?.[localVarOperationServerIndex]?.url;
            return (axios, basePath) => createRequestFunction(localVarAxiosArgs, globalAxios, BASE_PATH, configuration)(axios, localVarOperationServerBasePath || basePath);
        },
        /**
         * Get a patient from database by id.  Parameters ---------- patient_id     Id of the requested patient  Returns -------     Patient pydantic output model  Raises ------ HTTPException     404: Patient not found
         * @summary Get Patient
         * @param {number} patientId 
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        async getPatientApiV1PatientPatientIdGet(patientId: number, options?: RawAxiosRequestConfig): Promise<(axios?: AxiosInstance, basePath?: string) => AxiosPromise<PatientOut>> {
            const localVarAxiosArgs = await localVarAxiosParamCreator.getPatientApiV1PatientPatientIdGet(patientId, options);
            const localVarOperationServerIndex = configuration?.serverIndex ?? 0;
            const localVarOperationServerBasePath = operationServerMap['PatientsApi.getPatientApiV1PatientPatientIdGet']?.[localVarOperationServerIndex]?.url;
            return (axios, basePath) => createRequestFunction(localVarAxiosArgs, globalAxios, BASE_PATH, configuration)(axios, localVarOperationServerBasePath || basePath);
        },
        /**
         * Get all patients endpoint.  Returns -------     List of patient pydantic output models
         * @summary Get Patient List
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        async getPatientListApiV1PatientGet(options?: RawAxiosRequestConfig): Promise<(axios?: AxiosInstance, basePath?: string) => AxiosPromise<Array<PatientOut>>> {
            const localVarAxiosArgs = await localVarAxiosParamCreator.getPatientListApiV1PatientGet(options);
            const localVarOperationServerIndex = configuration?.serverIndex ?? 0;
            const localVarOperationServerBasePath = operationServerMap['PatientsApi.getPatientListApiV1PatientGet']?.[localVarOperationServerIndex]?.url;
            return (axios, basePath) => createRequestFunction(localVarAxiosArgs, globalAxios, BASE_PATH, configuration)(axios, localVarOperationServerBasePath || basePath);
        },
        /**
         * Update existing patient endpoint.  Parameters ---------- patient_id     Id of the patient to be updated payload     Patient data to be updated  Returns -------     Updated patient pydantic output model  Raises ------ HTTPException     404: Patient not found
         * @summary Update Patient
         * @param {number} patientId 
         * @param {BasePatient} basePatient 
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        async updatePatientApiV1PatientPatientIdPut(patientId: number, basePatient: BasePatient, options?: RawAxiosRequestConfig): Promise<(axios?: AxiosInstance, basePath?: string) => AxiosPromise<PatientOut>> {
            const localVarAxiosArgs = await localVarAxiosParamCreator.updatePatientApiV1PatientPatientIdPut(patientId, basePatient, options);
            const localVarOperationServerIndex = configuration?.serverIndex ?? 0;
            const localVarOperationServerBasePath = operationServerMap['PatientsApi.updatePatientApiV1PatientPatientIdPut']?.[localVarOperationServerIndex]?.url;
            return (axios, basePath) => createRequestFunction(localVarAxiosArgs, globalAxios, BASE_PATH, configuration)(axios, localVarOperationServerBasePath || basePath);
        },
    }
};

/**
 * PatientsApi - factory interface
 * @export
 */
export const PatientsApiFactory = function (configuration?: Configuration, basePath?: string, axios?: AxiosInstance) {
    const localVarFp = PatientsApiFp(configuration)
    return {
        /**
         * Create new patient database entry.  Parameters ---------- payload     Patient pydantic base model  Returns -------     Patient pydantic output model  Raises ------ HTTPException     404: Could not create patient
         * @summary Create Patient
         * @param {BasePatient} basePatient 
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        createPatientApiV1PatientPost(basePatient: BasePatient, options?: any): AxiosPromise<PatientOut> {
            return localVarFp.createPatientApiV1PatientPost(basePatient, options).then((request) => request(axios, basePath));
        },
        /**
         * Delete patient from database.  Parameters ---------- patient_id     Id of patient to be deleted  Raises ------ HTTPException     _description_
         * @summary Delete Patient
         * @param {number} patientId 
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        deletePatientApiV1PatientPatientIdDelete(patientId: number, options?: any): AxiosPromise<void> {
            return localVarFp.deletePatientApiV1PatientPatientIdDelete(patientId, options).then((request) => request(axios, basePath));
        },
        /**
         * Get a patient from database by id.  Parameters ---------- patient_id     Id of the requested patient  Returns -------     Patient pydantic output model  Raises ------ HTTPException     404: Patient not found
         * @summary Get Patient
         * @param {number} patientId 
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        getPatientApiV1PatientPatientIdGet(patientId: number, options?: any): AxiosPromise<PatientOut> {
            return localVarFp.getPatientApiV1PatientPatientIdGet(patientId, options).then((request) => request(axios, basePath));
        },
        /**
         * Get all patients endpoint.  Returns -------     List of patient pydantic output models
         * @summary Get Patient List
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        getPatientListApiV1PatientGet(options?: any): AxiosPromise<Array<PatientOut>> {
            return localVarFp.getPatientListApiV1PatientGet(options).then((request) => request(axios, basePath));
        },
        /**
         * Update existing patient endpoint.  Parameters ---------- patient_id     Id of the patient to be updated payload     Patient data to be updated  Returns -------     Updated patient pydantic output model  Raises ------ HTTPException     404: Patient not found
         * @summary Update Patient
         * @param {number} patientId 
         * @param {BasePatient} basePatient 
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        updatePatientApiV1PatientPatientIdPut(patientId: number, basePatient: BasePatient, options?: any): AxiosPromise<PatientOut> {
            return localVarFp.updatePatientApiV1PatientPatientIdPut(patientId, basePatient, options).then((request) => request(axios, basePath));
        },
    };
};

/**
 * PatientsApi - object-oriented interface
 * @export
 * @class PatientsApi
 * @extends {BaseAPI}
 */
export class PatientsApi extends BaseAPI {
    /**
     * Create new patient database entry.  Parameters ---------- payload     Patient pydantic base model  Returns -------     Patient pydantic output model  Raises ------ HTTPException     404: Could not create patient
     * @summary Create Patient
     * @param {BasePatient} basePatient 
     * @param {*} [options] Override http request option.
     * @throws {RequiredError}
     * @memberof PatientsApi
     */
    public createPatientApiV1PatientPost(basePatient: BasePatient, options?: RawAxiosRequestConfig) {
        return PatientsApiFp(this.configuration).createPatientApiV1PatientPost(basePatient, options).then((request) => request(this.axios, this.basePath));
    }

    /**
     * Delete patient from database.  Parameters ---------- patient_id     Id of patient to be deleted  Raises ------ HTTPException     _description_
     * @summary Delete Patient
     * @param {number} patientId 
     * @param {*} [options] Override http request option.
     * @throws {RequiredError}
     * @memberof PatientsApi
     */
    public deletePatientApiV1PatientPatientIdDelete(patientId: number, options?: RawAxiosRequestConfig) {
        return PatientsApiFp(this.configuration).deletePatientApiV1PatientPatientIdDelete(patientId, options).then((request) => request(this.axios, this.basePath));
    }

    /**
     * Get a patient from database by id.  Parameters ---------- patient_id     Id of the requested patient  Returns -------     Patient pydantic output model  Raises ------ HTTPException     404: Patient not found
     * @summary Get Patient
     * @param {number} patientId 
     * @param {*} [options] Override http request option.
     * @throws {RequiredError}
     * @memberof PatientsApi
     */
    public getPatientApiV1PatientPatientIdGet(patientId: number, options?: RawAxiosRequestConfig) {
        return PatientsApiFp(this.configuration).getPatientApiV1PatientPatientIdGet(patientId, options).then((request) => request(this.axios, this.basePath));
    }

    /**
     * Get all patients endpoint.  Returns -------     List of patient pydantic output models
     * @summary Get Patient List
     * @param {*} [options] Override http request option.
     * @throws {RequiredError}
     * @memberof PatientsApi
     */
    public getPatientListApiV1PatientGet(options?: RawAxiosRequestConfig) {
        return PatientsApiFp(this.configuration).getPatientListApiV1PatientGet(options).then((request) => request(this.axios, this.basePath));
    }

    /**
     * Update existing patient endpoint.  Parameters ---------- patient_id     Id of the patient to be updated payload     Patient data to be updated  Returns -------     Updated patient pydantic output model  Raises ------ HTTPException     404: Patient not found
     * @summary Update Patient
     * @param {number} patientId 
     * @param {BasePatient} basePatient 
     * @param {*} [options] Override http request option.
     * @throws {RequiredError}
     * @memberof PatientsApi
     */
    public updatePatientApiV1PatientPatientIdPut(patientId: number, basePatient: BasePatient, options?: RawAxiosRequestConfig) {
        return PatientsApiFp(this.configuration).updatePatientApiV1PatientPatientIdPut(patientId, basePatient, options).then((request) => request(this.axios, this.basePath));
    }
}



