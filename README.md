# Shipiqo Shipping for Odoo

Connect Odoo to **Shipiqo** — get real-time freight rates from 100+ carriers
directly in your sales orders, automatic shipment creation, live tracking, and
two-way carrier messaging.

## Requirements

- **Odoo 17.0** (use the `17.0` branch) or **Odoo 18.0** (use the `18.0` branch)
- An active **Shipiqo Pro** or **Enterprise** subscription
  → [Sign up here](https://shipiqo.com) (14-day free trial)
- Python `requests` library (included with Odoo)

> ⚠️ Free and Basic Shipiqo plans do **not** include Odoo integration.
> The module installs but rate lookups will return a tier upgrade prompt.

## Installation

### From the Odoo App Store
1. Go to **Apps** → search "Shipiqo Shipping"
2. Click **Install**

### From source
```bash
cd /path/to/odoo/addons
git clone -b 17.0 https://github.com/Shipiqo/shipiqo-odoo.git
# Restart Odoo, update apps list, install "Shipiqo Shipping"
```

## Setup (4 steps, ~2 minutes)

1. Install the module
2. Go to **Settings → Shipiqo → Connect**
3. Click **Authorize with Shipiqo** — you'll be redirected to your Shipiqo
   account to approve the connection and get an authorization code
4. Paste the code, test the connection, done

## Features

| Feature | Description |
|---------|-------------|
| Real-time rates | 100+ carriers across parcel, pallet, FTL, sea, air |
| Auto shipment creation | Triggered on sale order confirmation |
| Lifecycle widget | Live tracking, ETA, exceptions on sale orders |
| Two-way messaging | Chat with carriers from inside Odoo |
| Label printing | PDF and ZPL formats |
| International | EU, UK, US, Asia + customs |

## Supported Odoo versions

| Branch | Odoo version | Status |
|--------|--------------|--------|
| `17.0` | Odoo 17 | ✅ Stable |
| `18.0` | Odoo 18 | ✅ Stable |

## Subscription tiers

| Plan | Odoo integration | Other |
|------|------------------|-------|
| Free | ❌ | Web app only |
| Basic | ❌ | Web app + 1 widget |
| **Pro** | **✅** | Everything + Odoo |
| **Enterprise** | **✅** | Pro + white-label + dedicated support |

[See full pricing →](https://shipiqo.com/pricing)

## Support

- 📖 Documentation: https://shipiqo.com/docs/odoo
- 📧 Email: support@shipiqo.com
- 🐛 Issues: https://github.com/Shipiqo/shipiqo-odoo/issues

## License

OPL-1 — see [LICENSE](LICENSE).

© 2025 Shipiqo ApS
