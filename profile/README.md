# Say My Frame

[![pub package](https://img.shields.io/pub/v/smf_flutter_cli.svg)](https://pub.dev/packages/smf_flutter_cli)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=saymyframe_smf_flutter_cli&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=saymyframe_smf_flutter_cli)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=saymyframe_smf_flutter_cli&metric=coverage)](https://sonarcloud.io/component_measures?id=saymyframe_smf_flutter_cli&metric=coverage)
[![license](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/saymyframe/smf_flutter_cli/blob/main/LICENSE)
[![Join us on Discord](https://img.shields.io/badge/Join%20us-Discord-5865F2?logo=discord&logoColor=white)](https://saymyframe.com/discord)

Say My Frame (SMF) is a Flutter project generator whose modules are checked to work together. You pick what the app needs, such as a router, tabs at the bottom, dependency injection, a state manager or Firebase, and `smf create` generates a Flutter project that already has them wired up. CI checks this by generating apps from many combinations of modules and running `flutter analyze` on each of them.

Firebase goes all the way to `flutter build ipa`. SMF checks the machine for the Firebase CLI, a login and the FlutterFire CLI, and offers to set up what is missing and to run `flutterfire configure`. On macOS it also fixes the Crashlytics build phase, so `flutter build ipa` works with Swift Package Manager.

![smf create in a terminal: it asks for the app name and the modules, adds go_router and shared_preferences, which the chosen modules need, and generates a Flutter app with an onboarding, a start screen, a settings screen, tabs at the bottom, a theme, two languages, get_it and BLoC](https://doc.saymyframe.com/demo/0.4/smf_create.gif)

With the modules `onboarding`, `home`, `settings`, `bottom_tabs`, `material_theme` and `gen_l10n`, the app opens on an onboarding and has a start screen, a settings screen with a theme mode and a language, and a light and a dark theme:

![The app that smf create generates, on a phone: the onboarding, the start screen, the settings screen, and the start screen in the dark theme and in Ukrainian](https://doc.saymyframe.com/demo/app_look.png)

## Quick start

```bash
dart pub global activate smf_flutter_cli
smf create my_app -m home,onboarding,settings,bottom_tabs,material_theme,gen_l10n,get_it,bloc
```

`smf create` adds the modules that your choice needs, such as `go_router` for the start screen of `home` and `shared_preferences` for the onboarding. The app does not depend on SMF at run time, so its code is yours from the first commit.

SMF generates apps for Flutter 3.44 or newer and Dart 3.12 or newer. It is tested on macOS, Linux and Windows, and it is open source under the Apache License 2.0.

## Packages

[`smf_flutter_cli`](https://pub.dev/packages/smf_flutter_cli) is the Flutter CLI that installs the `smf` command. Each module is a package of its own, and you pick modules with `-m`:

| Module | Package | What it adds |
| --- | --- | --- |
| [`flutter_core`](https://doc.saymyframe.com/modules/flutter-core) | [`smf_flutter_core`](https://pub.dev/packages/smf_flutter_core) | The Flutter project for Android and iOS. Every app has it. |
| [`go_router`](https://doc.saymyframe.com/modules/go-router) | [`smf_go_router`](https://pub.dev/packages/smf_go_router) | Routes and typed navigation with go_router. |
| [`bottom_tabs`](https://doc.saymyframe.com/modules/bottom-tabs) | [`smf_bottom_tabs`](https://pub.dev/packages/smf_bottom_tabs) | Tabs in a bar at the bottom. |
| [`home`](https://doc.saymyframe.com/modules/home) | [`smf_home_flutter`](https://pub.dev/packages/smf_home_flutter) | A start screen that welcomes the developer of the app and lists the next steps. |
| [`onboarding`](https://doc.saymyframe.com/modules/onboarding) | [`smf_onboarding`](https://pub.dev/packages/smf_onboarding) | An onboarding on the first launch of the app. |
| [`settings`](https://doc.saymyframe.com/modules/settings) | [`smf_settings`](https://pub.dev/packages/smf_settings) | A settings screen with the settings of the modules, such as the theme mode and the language. |
| [`material_theme`](https://doc.saymyframe.com/modules/material-theme) | [`smf_material_theme`](https://pub.dev/packages/smf_material_theme) | A light and a dark Material 3 theme with a palette and a bundled font. |
| [`gen_l10n`](https://doc.saymyframe.com/modules/gen-l10n) | [`smf_gen_l10n`](https://pub.dev/packages/smf_gen_l10n) | The texts of the app in ARB files, with gen-l10n of Flutter. |
| [`shared_preferences`](https://doc.saymyframe.com/modules/shared-preferences) | [`smf_shared_preferences`](https://pub.dev/packages/smf_shared_preferences) | The settings of the app that are no secret, kept with shared_preferences. |
| [`bloc`](https://doc.saymyframe.com/modules/bloc) | [`smf_bloc`](https://pub.dev/packages/smf_bloc) | State management with flutter_bloc. |
| [`riverpod`](https://doc.saymyframe.com/modules/riverpod) | [`smf_riverpod`](https://pub.dev/packages/smf_riverpod) | State management with flutter_riverpod. |
| [`get_it`](https://doc.saymyframe.com/modules/get-it) | [`smf_get_it`](https://pub.dev/packages/smf_get_it) | Dependency injection with get_it. |
| [`event_bus`](https://doc.saymyframe.com/modules/event-bus) | [`smf_event_bus`](https://pub.dev/packages/smf_event_bus) | Events between parts of the app, with event_bus. |
| [`firebase_core`](https://doc.saymyframe.com/modules/firebase-core) | [`smf_firebase_core`](https://pub.dev/packages/smf_firebase_core) | Firebase, set up with `flutterfire configure`. |
| [`firebase_crashlytics`](https://doc.saymyframe.com/modules/firebase-crashlytics) | [`smf_firebase_crashlytics`](https://pub.dev/packages/smf_firebase_crashlytics) | Crash reporting with Firebase Crashlytics. |
| [`firebase_analytics`](https://doc.saymyframe.com/modules/firebase-analytics) | [`smf_firebase_analytics`](https://pub.dev/packages/smf_firebase_analytics) | Analytics with Firebase Analytics and, with a router, a screen view for each screen. |

## Modules of your own

A module is a Dart package built on [`smf_contracts`](https://pub.dev/packages/smf_contracts), the module model. It names the roles it needs, such as a router, rather than the modules that provide them. [`smf_pipeline`](https://pub.dev/packages/smf_pipeline) is the generation pipeline and has a contract harness for testing modules, and `runCli` in `smf_flutter_cli` lets you offer them in a command of your own. [Extending SMF](https://doc.saymyframe.com/extending) covers the details.

## Links

[Website](https://saymyframe.com) · [Documentation](https://doc.saymyframe.com) · [GitHub](https://github.com/saymyframe/smf_flutter_cli) · [Issues](https://github.com/saymyframe/smf_flutter_cli/issues) · [Discord](https://saymyframe.com/discord)
