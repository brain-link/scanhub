import 'regenerator-runtime/runtime'
import type { SubscribeFunction } from 'relay-runtime'
import { Environment, Observable, RecordSource, Store } from 'relay-runtime'
import {
  RelayNetworkLayer,
  cacheMiddleware,
  uploadMiddleware,
  urlMiddleware,
} from 'react-relay-network-modern'
import { SubscriptionClient } from 'subscriptions-transport-ws'

const subscriptionClient = new SubscriptionClient(
  'ws://127.0.0.1:8000',
  {
    reconnect: true,
  }
)

const subscribeFn: SubscribeFunction = (request, variables) => {
  const subscribeObservable = subscriptionClient.request({
    query: request.text,
    operationName: request.name,
    variables,
  })
  // Important: Convert subscriptions-transport-ws observable type to Relay's
  return Observable.create(({ next, error, complete }) => {
    subscribeObservable.subscribe({ next, error, complete })
  })
}

const network = new RelayNetworkLayer(
  [
    urlMiddleware({
      url: '/graphql',
    }),
    cacheMiddleware({
      size: 100, // max 100 requests
      ttl: 900000, // 15 minutes
    }),
    uploadMiddleware(),
  ],
  {
    // @ts-expect-error SubscribeFunction types don't match here
    subscribeFn,
  },
)

const source = new RecordSource()
const store = new Store(source)
export const environment = new Environment({ network, store })
