#!/usr/bin/env node

import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import process from 'node:process';
import readline from 'node:readline/promises';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const ROOT = path.resolve(__dirname, '..');
const VERSIONS_DIR = path.join(ROOT, 'versions');
const SKILL_NAME = 'exact-ui-replica';
const DISPLAY_NAME = 'Exact UI Replica';

const AGENTS = {
  claude: {
    label: 'Claude Code',
    user: () => path.join(os.homedir(), '.claude', 'skills', SKILL_NAME),
    project: cwd => path.join(cwd, '.claude', 'skills', SKILL_NAME),
    markers: cwd => [path.join(cwd, '.claude'), path.join(os.homedir(), '.claude')],
  },
  codex: {
    label: 'Codex',
    user: () => path.join(os.homedir(), '.agents', 'skills', SKILL_NAME),
    project: cwd => path.join(cwd, '.agents', 'skills', SKILL_NAME),
    markers: cwd => [path.join(cwd, '.agents'), path.join(os.homedir(), '.agents')],
  },
};

function banner() {
  console.log('\nWisdom\nPortable skills for AI coding agents.\n');
}

function printHelp() {
  console.log(`Usage:
  npx wisdom install
  npx wisdom <command> [options]

Commands:
  install      Install a skill into an AI coding tool
  update       Update an installed skill
  uninstall    Remove an installed skill
  doctor       Check detected tools and installations
  list         List bundled skills and versions
  help         Show this help

Options:
  --agent <claude|codex|all>   Installation target
  --scope <project|user>       Current project or global installation
  --version <version|latest>   Skill release (default: latest)
  --project <path>             Project root (default: current directory)
  --force                      Replace an existing installation
  --yes                        Accept detected/default choices
  --json                       Machine-readable output

Quick start:
  From your project root, run npx wisdom install
`);
}

function fail(message, code = 1) {
  console.error(`Error: ${message}`);
  process.exit(code);
}

function parseArgs(argv) {
  const command = argv[0] && !argv[0].startsWith('-') ? argv[0] : 'install';
  const start = command === 'install' && argv[0]?.startsWith('-') ? 0 : 1;
  const out = { command, agent: null, scope: null, version: 'latest', project: process.cwd(), force: false, yes: false, json: false };
  for (let i = start; i < argv.length; i++) {
    const arg = argv[i];
    if (arg === '--force') out.force = true;
    else if (arg === '--yes' || arg === '-y') out.yes = true;
    else if (arg === '--json') out.json = true;
    else if (['--agent', '--scope', '--version', '--project'].includes(arg)) {
      const value = argv[++i];
      if (!value) fail(`Missing value for ${arg}`);
      out[arg.slice(2)] = value;
    } else if (['--help', '-h'].includes(arg)) out.command = 'help';
    else fail(`Unknown option: ${arg}`);
  }
  return out;
}

function compareSemver(a, b) {
  const pa = a.split('.').map(Number);
  const pb = b.split('.').map(Number);
  for (let i = 0; i < 3; i++) if (pa[i] !== pb[i]) return pa[i] - pb[i];
  return 0;
}

function versions() {
  if (!fs.existsSync(VERSIONS_DIR)) fail(`Bundled versions directory not found: ${VERSIONS_DIR}`);
  return fs.readdirSync(VERSIONS_DIR, { withFileTypes: true })
    .filter(entry => entry.isDirectory() && /^v?\d+\.\d+\.\d+$/.test(entry.name))
    .map(entry => entry.name.replace(/^v/, ''))
    .sort(compareSemver);
}

function resolveVersion(requested) {
  const available = versions();
  if (!available.length) fail('No bundled skill versions found.');
  const version = requested === 'latest' ? available.at(-1) : requested.replace(/^v/, '');
  if (!available.includes(version)) fail(`Version ${requested} is unavailable. Available: ${available.join(', ')}`);
  return version;
}

function sourceFor(version) {
  const source = path.join(VERSIONS_DIR, `v${version}`);
  if (!fs.existsSync(path.join(source, 'SKILL.md'))) fail(`Invalid release v${version}: SKILL.md is missing.`);
  return source;
}

function detectAgents(project) {
  return Object.entries(AGENTS)
    .filter(([, config]) => config.markers(project).some(marker => fs.existsSync(marker)))
    .map(([name]) => name);
}

async function askChoice(question, choices, defaultIndex = 0) {
  const rl = readline.createInterface({ input: process.stdin, output: process.stdout });
  console.log(question);
  choices.forEach((choice, index) => console.log(`  ${index + 1}. ${choice.label}`));
  const answer = (await rl.question(`Choose [${defaultIndex + 1}]: `)).trim();
  rl.close();
  if (!answer) return choices[defaultIndex].value;
  const index = Number(answer) - 1;
  if (!Number.isInteger(index) || !choices[index]) fail('Invalid selection.');
  return choices[index].value;
}

async function resolveInteractiveOptions(opts) {
  const detected = detectAgents(path.resolve(opts.project));
  if (!opts.agent) {
    if (opts.yes) opts.agent = detected.length === 1 ? detected[0] : 'claude';
    else {
      const choices = [
        { label: 'Claude Code', value: 'claude' },
        { label: 'Codex', value: 'codex' },
        { label: 'All supported tools', value: 'all' },
      ];
      const defaultIndex = detected.length === 1 ? choices.findIndex(c => c.value === detected[0]) : 0;
      opts.agent = await askChoice('Where should Wisdom install the skill?', choices, Math.max(defaultIndex, 0));
    }
  }
  if (!opts.scope) {
    if (opts.yes) opts.scope = 'project';
    else opts.scope = await askChoice('Installation scope?', [
      { label: 'This project (recommended)', value: 'project' },
      { label: 'My computer (all projects)', value: 'user' },
    ]);
  }
  return opts;
}

function selectedAgents(value) {
  if (value === 'all') return Object.keys(AGENTS);
  if (!AGENTS[value]) fail(`Unsupported agent: ${value}. Use claude, codex, or all.`);
  return [value];
}

function destination(agent, scope, project) {
  if (!['user', 'project'].includes(scope)) fail(`Unsupported scope: ${scope}. Use project or user.`);
  return AGENTS[agent][scope](path.resolve(project));
}

function copyDir(source, target) {
  fs.mkdirSync(path.dirname(target), { recursive: true });
  fs.cpSync(source, target, {
    recursive: true,
    force: true,
    filter: src => !src.includes(`${path.sep}__pycache__`) && !src.endsWith('.pyc') && !src.includes(`${path.sep}node_modules${path.sep}`),
  });
}

function installedVersion(target) {
  const versionFile = path.join(target, 'VERSION');
  if (fs.existsSync(versionFile)) return fs.readFileSync(versionFile, 'utf8').trim();
  try { return JSON.parse(fs.readFileSync(path.join(target, 'skill.json'), 'utf8')).version || 'unknown'; }
  catch { return 'unknown'; }
}

function validateSource(source) {
  const required = ['SKILL.md', 'README.md', 'skill.json'];
  const missing = required.filter(file => !fs.existsSync(path.join(source, file)));
  if (missing.length) fail(`Release validation failed. Missing: ${missing.join(', ')}`);
  const skill = fs.readFileSync(path.join(source, 'SKILL.md'), 'utf8');
  if (!skill.startsWith('---') || !skill.includes(`name: ${SKILL_NAME}`)) fail('Release validation failed: malformed SKILL.md frontmatter.');
}

function output(opts, data, human) {
  if (opts.json) console.log(JSON.stringify(data, null, 2));
  else human();
}

function install(opts, updating = false) {
  const version = resolveVersion(opts.version);
  const source = sourceFor(version);
  validateSource(source);
  const results = [];
  for (const agent of selectedAgents(opts.agent)) {
    const target = destination(agent, opts.scope, opts.project);
    const exists = fs.existsSync(target);
    if (exists && !opts.force && !updating) fail(`${AGENTS[agent].label} already has this skill at ${target}. Run update or add --force.`);
    if (exists) fs.rmSync(target, { recursive: true, force: true });
    copyDir(source, target);
    results.push({ agent, scope: opts.scope, version, path: target, status: exists ? 'replaced' : 'installed' });
  }
  output(opts, { success: true, command: updating ? 'update' : 'install', skill: SKILL_NAME, results }, () => {
    console.log('');
    for (const item of results) console.log(`✓ ${DISPLAY_NAME} v${item.version} installed for ${AGENTS[item.agent].label}\n  ${item.path}`);
    console.log('\nInside your AI coding tool, say:\n  “Use Exact UI Replica to recreate this MVP exactly.”\n');
  });
}

function uninstall(opts) {
  const results = [];
  for (const agent of selectedAgents(opts.agent)) {
    const target = destination(agent, opts.scope, opts.project);
    const existed = fs.existsSync(target);
    if (existed) fs.rmSync(target, { recursive: true, force: true });
    results.push({ agent, scope: opts.scope, path: target, status: existed ? 'removed' : 'not-installed' });
  }
  output(opts, { success: true, command: 'uninstall', results }, () => {
    results.forEach(item => console.log(`${item.status === 'removed' ? '✓' : '•'} ${AGENTS[item.agent].label}: ${item.status}\n  ${item.path}`));
  });
}

function doctor(opts) {
  const detected = detectAgents(path.resolve(opts.project));
  const checks = [];
  for (const agent of Object.keys(AGENTS)) {
    for (const scope of ['project', 'user']) {
      const target = destination(agent, scope, opts.project);
      checks.push({ agent, scope, path: target, installed: fs.existsSync(path.join(target, 'SKILL.md')), version: fs.existsSync(target) ? installedVersion(target) : null });
    }
  }
  output(opts, { success: true, node: process.version, detectedAgents: detected, bundledVersions: versions(), checks }, () => {
    console.log(`Node: ${process.version}`);
    console.log(`Detected: ${detected.length ? detected.map(a => AGENTS[a].label).join(', ') : 'No agent folders detected yet'}`);
    console.log(`Bundled skill versions: ${versions().map(v => `v${v}`).join(', ')}\n`);
    checks.forEach(check => console.log(`${check.installed ? '✓' : '•'} ${AGENTS[check.agent].label} ${check.scope}: ${check.installed ? `v${check.version}` : 'not installed'}\n  ${check.path}`));
  });
}

function list(opts) {
  const available = versions();
  output(opts, { success: true, skills: [{ name: SKILL_NAME, displayName: DISPLAY_NAME, versions: available, latest: available.at(-1) }] }, () => {
    console.log(`${DISPLAY_NAME}\n  id: ${SKILL_NAME}\n  versions: ${available.map(v => `v${v}`).join(', ')}\n  latest: v${available.at(-1)}`);
  });
}

const opts = parseArgs(process.argv.slice(2));
if (!opts.json) banner();

switch (opts.command) {
  case 'install': await resolveInteractiveOptions(opts); install(opts); break;
  case 'update': await resolveInteractiveOptions(opts); install({ ...opts, force: true }, true); break;
  case 'uninstall': await resolveInteractiveOptions(opts); uninstall(opts); break;
  case 'doctor': doctor(opts); break;
  case 'list': list(opts); break;
  case 'help': printHelp(); break;
  default: printHelp(); fail(`Unknown command: ${opts.command}`);
}
