/**
 * @generated SignedSource<<8ac721a830c519e3ed977b5201434a33>>
 * @lightSyntaxTransform
 * @nogrep
 */

/* tslint:disable */
/* eslint-disable */
// @ts-nocheck

import { ConcreteRequest, Query } from 'relay-runtime';
export type PatientSex = "NONE" | "MALE" | "FEMALE" | "DIVERSE" | "%future added value";
export type PatientStatus = "NEW" | "RECORDING" | "DIAGNOSIS" | "%future added value";
export type ClientQuery$variables = {};
export type ClientQuery$data = {
  readonly me: {
    readonly id: string;
    readonly name: string;
    readonly age: number;
  } | null;
  readonly allPatients: ReadonlyArray<{
    readonly id: string;
    readonly sex: PatientSex;
    readonly birthday: string;
    readonly concern: string;
    readonly admissionDate: string;
    readonly status: PatientStatus;
  }>;
  readonly getPatient: {
    readonly id: string;
    readonly sex: PatientSex;
    readonly birthday: string;
    readonly concern: string;
    readonly admissionDate: string;
    readonly status: PatientStatus;
  };
};
export type ClientQuery = {
  variables: ClientQuery$variables;
  response: ClientQuery$data;
};

const node: ConcreteRequest = (function(){
var v0 = {
  "alias": null,
  "args": null,
  "kind": "ScalarField",
  "name": "id",
  "storageKey": null
},
v1 = [
  (v0/*: any*/),
  {
    "alias": null,
    "args": null,
    "kind": "ScalarField",
    "name": "sex",
    "storageKey": null
  },
  {
    "alias": null,
    "args": null,
    "kind": "ScalarField",
    "name": "birthday",
    "storageKey": null
  },
  {
    "alias": null,
    "args": null,
    "kind": "ScalarField",
    "name": "concern",
    "storageKey": null
  },
  {
    "alias": null,
    "args": null,
    "kind": "ScalarField",
    "name": "admissionDate",
    "storageKey": null
  },
  {
    "alias": null,
    "args": null,
    "kind": "ScalarField",
    "name": "status",
    "storageKey": null
  }
],
v2 = [
  {
    "alias": null,
    "args": null,
    "concreteType": "User",
    "kind": "LinkedField",
    "name": "me",
    "plural": false,
    "selections": [
      (v0/*: any*/),
      {
        "alias": null,
        "args": null,
        "kind": "ScalarField",
        "name": "name",
        "storageKey": null
      },
      {
        "alias": null,
        "args": null,
        "kind": "ScalarField",
        "name": "age",
        "storageKey": null
      }
    ],
    "storageKey": null
  },
  {
    "alias": null,
    "args": null,
    "concreteType": "Patient",
    "kind": "LinkedField",
    "name": "allPatients",
    "plural": true,
    "selections": (v1/*: any*/),
    "storageKey": null
  },
  {
    "alias": null,
    "args": [
      {
        "kind": "Literal",
        "name": "id",
        "value": 20
      }
    ],
    "concreteType": "Patient",
    "kind": "LinkedField",
    "name": "getPatient",
    "plural": false,
    "selections": (v1/*: any*/),
    "storageKey": "getPatient(id:20)"
  }
];
return {
  "fragment": {
    "argumentDefinitions": [],
    "kind": "Fragment",
    "metadata": null,
    "name": "ClientQuery",
    "selections": (v2/*: any*/),
    "type": "Query",
    "abstractKey": null
  },
  "kind": "Request",
  "operation": {
    "argumentDefinitions": [],
    "kind": "Operation",
    "name": "ClientQuery",
    "selections": (v2/*: any*/)
  },
  "params": {
    "cacheID": "1a908fd15329f8c342b74d8862f70a89",
    "id": null,
    "metadata": {},
    "name": "ClientQuery",
    "operationKind": "query",
    "text": "query ClientQuery {\n  me {\n    id\n    name\n    age\n  }\n  allPatients {\n    id\n    sex\n    birthday\n    concern\n    admissionDate\n    status\n  }\n  getPatient(id: 20) {\n    id\n    sex\n    birthday\n    concern\n    admissionDate\n    status\n  }\n}\n"
  }
};
})();

(node as any).hash = "e371b75f51630237f379faa433f825a5";

export default node;
