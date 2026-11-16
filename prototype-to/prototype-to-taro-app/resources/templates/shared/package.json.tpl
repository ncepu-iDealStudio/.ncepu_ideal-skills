{
  "name": "{{project_name}}",
  "version": "1.0.0",
  "private": true,
  "description": "{{app_title}}",
  "templateInfo": {
    "name": "default",
    "typescript": true,
    "css": "sass",
    "framework": "{{framework}}"
  },
  "scripts": {
    "dev:weapp": "taro build --type weapp --watch",
    "dev:h5": "taro build --type h5 --watch",
    "dev:alipay": "taro build --type alipay --watch",
    "build:weapp": "taro build --type weapp",
    "build:h5": "taro build --type h5",
    "type-check": "tsc --noEmit"
  },
  "browserslist": ["last 3 versions", "Android >= 4.1", "ios >= 8"],
  "dependencies": {},
  "devDependencies": {}
}
