<script lang="ts">
  import { navigate, type Route } from './lib/router';

  interface Props {
    currentRoute: Route;
  }

  let { currentRoute }: Props = $props();

  const navItems: { route: Route; number: string; label: string; muted?: boolean }[] = [
    { route: 'dashboard',  number: '00', label: 'All tools' },
    { route: 'energy',     number: '01', label: 'Energy & wavelength' },
    { route: 'intensity',  number: '02', label: 'Intensity & fluence' },
    { route: 'eta',        number: '03', label: 'η / η′ per atom' },
    { route: 'omega',      number: '04', label: 'Solid angle' },
    { route: 'about',      number: '05', label: 'Formulas' },
  ];
</script>

<aside class="sidebar">
  <div class="header">
    <div class="logo">Lab<br>Tools</div>
    <div class="tagline">Calculators for XFEL nanofocus experiments</div>
  </div>

  <nav>
    {#each navItems as item}
      <button
        class="nav-item"
        class:active={currentRoute === item.route}
        onclick={() => navigate(item.route)}
      >
        <span class="indicator">
          {#if currentRoute === item.route}
            <span class="indicator-bar"></span>
          {/if}
        </span>
        <span class="number">{item.number}</span>
        <span class="label" class:muted-label={item.muted}>{item.label}</span>
      </button>
    {/each}
  </nav>

  <div class="footer">
    <div class="footer-text">static · no backend</div>
  </div>
</aside>

<style>
  .sidebar {
    width: var(--sidebar-width);
    flex: none;
    background: var(--color-sidebar);
    color: var(--color-sidebar-text);
    display: flex;
    flex-direction: column;
    position: sticky;
    top: 0;
    height: 100vh;
  }

  .header {
    padding: 34px 26px 26px;
  }

  .logo {
    font-family: var(--font-ui);
    font-weight: 600;
    font-size: 27px;
    line-height: 0.92;
    letter-spacing: -0.025em;
    text-transform: uppercase;
  }

  .tagline {
    margin-top: 12px;
    font-family: var(--font-mono);
    font-size: 11.5px;
    line-height: 1.55;
    color: var(--color-sidebar-muted);
  }

  nav {
    display: flex;
    flex-direction: column;
    padding: 6px 0;
    border-top: 1px solid var(--color-sidebar-border);
  }

  .nav-item {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 13px 26px 13px 0;
    background: transparent;
    border: 0;
    border-bottom: 1px solid rgba(237, 231, 218, 0.08);
    cursor: pointer;
    text-align: left;
    color: var(--color-sidebar-text);
  }

  .nav-item:last-child {
    border-bottom: 0;
  }

  .nav-item:hover {
    background: var(--color-sidebar-hover);
  }

  .indicator {
    width: 3px;
    height: 20px;
    flex: none;
    display: block;
  }

  .indicator-bar {
    display: block;
    width: 3px;
    height: 20px;
    background: var(--color-accent);
  }

  .number {
    font-family: var(--font-mono);
    font-size: 10.5px;
    color: var(--color-sidebar-nav-muted);
    width: 20px;
  }

  .label {
    font-family: var(--font-ui);
    font-weight: 500;
    font-size: 13.5px;
    letter-spacing: 0.005em;
  }

  .muted-label {
    color: var(--color-sidebar-muted);
  }

  .footer {
    margin-top: auto;
    padding: 22px 26px 26px;
    border-top: 1px solid var(--color-sidebar-border);
  }

  .footer-text {
    font-family: var(--font-mono);
    font-size: 10.5px;
    line-height: 1.5;
    color: var(--color-sidebar-nav-muted);
  }
</style>
