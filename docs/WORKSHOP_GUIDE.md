# LLM Poisoning Workshop - Facilitator Guide

## Workshop Overview

**Duration**: 8 hours (full day workshop)  
**Audience**: Senior engineers, security professionals, AI/ML practitioners  
**Level**: Advanced  
**Prerequisites**: 
- Understanding of LLM concepts
- Python programming experience
- Cloud computing basics
- Security fundamentals

## Learning Objectives

By the end of this workshop, participants will be able to:
1. Identify vulnerabilities in LLM-based systems
2. Execute common poisoning attacks in controlled environments
3. Implement protection strategies using Microsoft solutions
4. Design secure RAG architectures
5. Establish monitoring and response procedures

## Workshop Structure

### Part 1: Foundation (2 hours)

#### Module 1: Theory (45 minutes)
**Presentation**: Introduction to LLM Poisoning
- What is LLM poisoning?
- Types of attacks
- Real-world examples
- Business impact

**Activity**: Group discussion on attack scenarios
- Break into groups of 3-4
- Each group analyzes a different attack scenario
- Present findings (5 minutes per group)

**Materials Needed**:
- Slides: docs/01-theory.md
- Handout: Attack scenario cards
- Whiteboard for group presentations

#### Module 2: Microsoft AI Stack (45 minutes)
**Presentation**: Architecture Overview
- Azure OpenAI Service
- Azure AI Foundry
- Azure AI Search
- Integration patterns

**Demo**: Live walkthrough of Azure AI services
- Show Azure Portal
- Demonstrate OpenAI Studio
- Show AI Search interface
- Explain security features

**Activity**: Architecture mapping
- Participants diagram their own systems
- Identify potential attack surfaces
- Share with the group

#### Break (15 minutes)

#### Module 3: Environment Setup (30 minutes)
**Hands-on**: Deploy Azure resources
- Run deployment script
- Verify resource creation
- Configure local environment
- Test connections

**Troubleshooting**:
- Have backup Azure subscriptions ready
- Pre-deploy resources if time is limited
- Provide shared resources for participants with issues

### Part 2: Attack Demonstrations (2.5 hours)

#### Lab 1: Deploy Vulnerable Application (45 minutes)
**Objectives**:
- Deploy the sample HR chatbot
- Explore functionality
- Identify vulnerabilities
- Document attack surface

**Facilitation Tips**:
- Walk through deployment together
- Pause for questions
- Have participants share what they find
- Encourage exploration

**Key Points to Emphasize**:
- Why these vulnerabilities exist
- How common they are in real systems
- The importance of secure defaults

#### Lab 2: RAG Poisoning Attack (45 minutes)
**Objectives**:
- Inject malicious documents
- Observe before/after behavior
- Measure impact
- Document findings

**Demo**: Live attack execution
1. Show clean system behavior
2. Execute poisoning script
3. Show compromised behavior
4. Discuss detection challenges

**Activity**: Participants execute attack
- Follow lab guide
- Document results
- Compare with neighbors
- Discuss implications

**Discussion Questions**:
- How would you detect this in production?
- What's the blast radius of this attack?
- How long until someone notices?

#### Break (15 minutes)

#### Module 4: Prompt Injection (45 minutes)
**Presentation**: Types of prompt injection
- Direct injection
- Indirect injection
- Multi-turn attacks
- Advanced techniques

**Demo**: Live prompt injection attempts
- Show successful injections
- Show failed attempts
- Explain why some work and others don't

**Activity**: Injection challenge
- Provide target system
- Participants try different injection techniques
- Award points for successful attacks
- Discuss most effective methods

### Lunch Break (60 minutes)

### Part 3: Protection Strategies (2 hours)

#### Module 5: Input Validation (45 minutes)
**Presentation**: Validation techniques
- Length and character validation
- Pattern detection
- Semantic validation
- Best practices

**Code Review**: Input validator implementation
- Walk through code together
- Explain each validation layer
- Discuss trade-offs

**Activity**: Implement basic validator
- Participants code a simple validator
- Test against known attacks
- Measure effectiveness

#### Module 6: Complete Protection (45 minutes)
**Presentation**: Multi-layer defense
- Content filtering
- Output monitoring
- Access controls
- Audit logging

**Demo**: Protected system
- Show same attacks against protected system
- Explain why they fail
- Discuss remaining risks

**Activity**: Lab 3 - Implement Protections
- Add input validation
- Configure content filters
- Enable monitoring
- Test effectiveness

#### Break (15 minutes)

#### Module 7: Monitoring and Detection (30 minutes)
**Presentation**: Production monitoring
- What to log
- Alert configuration
- Anomaly detection
- Incident response

**Demo**: Azure Monitor integration
- Show Application Insights
- Configure alert rules
- Review sample incidents
- Demonstrate response workflow

### Part 4: Advanced Topics and Wrap-up (1.5 hours)

#### Module 8: Real-World Case Studies (30 minutes)
**Presentation**: Industry examples
- Case study 1: ChatGPT injection attacks
- Case study 2: Bing Chat manipulation
- Case study 3: Enterprise RAG compromise
- Lessons learned

**Discussion**: Participant experiences
- Have participants seen similar issues?
- What worked in their organizations?
- What challenges remain?

#### Module 9: Future Threats (20 minutes)
**Presentation**: Emerging risks
- Automated attack tools
- AI-powered adversaries
- Supply chain attacks
- Regulatory landscape

**Activity**: Threat modeling
- Groups identify future threats
- Propose mitigations
- Share with class

#### Module 10: Best Practices and Q&A (40 minutes)
**Presentation**: Security framework
- Design principles
- Development lifecycle integration
- Testing strategies
- Continuous improvement

**Open Discussion**:
- Answer remaining questions
- Discuss implementation challenges
- Share resources
- Network with peers

## Materials Checklist

### Pre-Workshop
- [ ] Azure subscriptions for all participants
- [ ] Pre-deployed resources (backup)
- [ ] Workshop repository cloned on all machines
- [ ] Printed lab guides
- [ ] Scenario cards
- [ ] Name tags and sign-in sheet

### During Workshop
- [ ] Projector and screen
- [ ] Whiteboard and markers
- [ ] Post-it notes for activities
- [ ] Power strips for laptops
- [ ] WiFi credentials
- [ ] Refreshments and lunch arrangements

### Post-Workshop
- [ ] Feedback forms
- [ ] Certificate of completion
- [ ] Additional resources list
- [ ] Contact information for support
- [ ] Resource cleanup instructions

## Timing Guidelines

| Time | Activity | Duration |
|------|----------|----------|
| 8:00 | Registration & Setup | 30 min |
| 8:30 | Module 1: Theory | 45 min |
| 9:15 | Module 2: Microsoft Stack | 45 min |
| 10:00 | Break | 15 min |
| 10:15 | Module 3: Environment Setup | 30 min |
| 10:45 | Lab 1: Vulnerable App | 45 min |
| 11:30 | Lab 2: RAG Poisoning | 45 min |
| 12:15 | Lunch | 60 min |
| 1:15 | Module 4: Prompt Injection | 45 min |
| 2:00 | Module 5: Input Validation | 45 min |
| 2:45 | Break | 15 min |
| 3:00 | Module 6: Complete Protection | 45 min |
| 3:45 | Module 7: Monitoring | 30 min |
| 4:15 | Module 8: Case Studies | 30 min |
| 4:45 | Module 9: Future Threats | 20 min |
| 5:05 | Module 10: Best Practices & Q&A | 40 min |
| 5:45 | Wrap-up & Feedback | 15 min |
| 6:00 | End | |

## Facilitation Tips

### Engagement Strategies
1. **Start with a hook**: Begin with a real-world incident
2. **Vary activities**: Mix presentations, demos, and hands-on
3. **Encourage questions**: Create safe space for learning
4. **Use analogies**: Compare to familiar security concepts
5. **Show, don't just tell**: Live demos are more impactful

### Common Challenges

**Challenge**: Participants at different skill levels
**Solution**: 
- Provide optional advanced exercises
- Pair experienced with less experienced
- Have extension activities ready

**Challenge**: Technical issues with Azure
**Solution**:
- Have backup pre-deployed environments
- Provide shared resources
- Have troubleshooting guide ready

**Challenge**: Running behind schedule
**Solution**:
- Identify optional sections to skip
- Combine similar modules
- Extend lunch break if needed

**Challenge**: Sensitive security discussions
**Solution**:
- Emphasize educational purpose
- Remind about legal/ethical boundaries
- Keep focus on defensive measures

### Assessment

**Formative Assessment** (during workshop):
- Observe lab completion
- Check understanding during discussions
- Review vulnerability findings
- Evaluate protection implementations

**Summative Assessment** (end of workshop):
- Lab completion certificate
- Optional quiz on key concepts
- Capstone exercise: Design secure system

**Feedback Collection**:
- Mid-day pulse check
- End-of-day survey
- Follow-up email after 1 week

## Resources for Participants

### Provided Materials
- Complete workshop repository
- Lab guides and solutions
- Slide decks
- Reference architecture diagrams
- Security checklists

### Additional Resources
- OWASP LLM Top 10
- Microsoft AI security documentation
- Research papers on LLM security
- Online communities and forums
- Security tool recommendations

## Follow-up

### Immediate (Day After)
- Email thank you and feedback form
- Share additional resources
- Provide support contact

### Short-term (1 Week)
- Check on implementation progress
- Answer follow-up questions
- Share community updates

### Long-term (1 Month+)
- Advanced workshop announcement
- Community meetup invitation
- Update materials based on feedback

## Evaluation Metrics

### Success Indicators
- 90%+ completion rate for labs
- Average feedback score > 4/5
- 80%+ would recommend
- Participants implement learnings

### Areas to Measure
- Content relevance
- Pace appropriateness
- Instructor effectiveness
- Hands-on usefulness
- Overall satisfaction

## Continuous Improvement

**After Each Workshop**:
1. Review feedback forms
2. Update materials based on comments
3. Refresh examples with current events
4. Test all labs in clean environment
5. Update resource links

**Quarterly**:
1. Review attack landscape
2. Add new scenarios
3. Update protection strategies
4. Refresh case studies

**Annually**:
1. Major content revision
2. Update for new technologies
3. Incorporate regulatory changes
4. Benchmark against industry

## Emergency Contacts

- Azure Support: [Number]
- IT Support: [Number]
- Venue Contact: [Number]
- Emergency Services: 911

## Legal and Compliance

### Disclaimers
- Educational use only
- No production testing
- Follow acceptable use policies
- Report vulnerabilities responsibly

### Confidentiality
- Workshop content is public
- Participant data is confidential
- Organization-specific discussions stay private
- No recording without consent

## Version History

- v1.0 (2024-01): Initial workshop
- v1.1 (2024-02): Added case studies
- v1.2 (2024-03): Updated for GPT-4

---

**For questions or support, contact**: workshop@company.com
