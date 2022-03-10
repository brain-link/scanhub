module.exports = {
  projects: {
    'test-client': {
      schema: ['./apps/test-client/schema.graphql'],
      include: ['**/*.{ts,tsx}'],
      extensions: {
        languageService: {
          cacheSchemaFileForLookup: true,
          useSchemaFileDefinitions: true,
        },
        endpoints: {
          default: {
            url: 'http://localhost:8000',
            subscriptionUrl: 'ws://localhost:8000',
          }
        }
      }
    }
  }
}