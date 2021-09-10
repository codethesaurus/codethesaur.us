# Security Policy

1. [Reporting security problems](#reporting)
2. [Security Point of Contact](#contact)
3. [Incident Response Process](#process)

<a name="reporting"></a>
## Reporting Security Problems

**DO NOT CREATE AN ISSUE** to report a security problem. Instead, please
send an email to coreteam@codethesaur.us.

<a name="contact"></a>
## Security Point of Contact

The security point of contact is Sarah Withee. Sarah responds to security
incident reports as fast as possible, within one business day at the latest.

If she doesn't respond within two days, please try emailing again.

<a name="process"></a>
## Incident Response Process

In case an incident is discovered or reported, I will follow the following
process to contain, respond and remediate:

### 1. Containment

The first step is to find out the root cause, nature and scope of the incident.

- Is still ongoing? If yes, first priority is to stop it.
- Is the incident outside of my influence? If yes, first priority is to contain it.
- Find out knows about the incident and who is affected.
- Find out what data was potentially exposed.

One way to immediately remove all access for the WIP app is to remove the
private key from the WIP App Settings page. The access can be recovered later
by generating a new private key and re-deploy the app.

### 2. Response

After the initial assessment and containment to my best abilities, I will
document all actions taken in a response plan.

I will create a comment in [the issues](https://github.com/codethesaurus/codethesaur.us/issues) to inform users about
the incident and what I actions I took to contain it.

### 3. Remediation

Once the incident is confirmed to be resolved, I will summarize the lessons
learned from the incident and create a list of actions I will take to prevent
it from happening again.
