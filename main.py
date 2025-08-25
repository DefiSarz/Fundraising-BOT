class ScamRisk(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ProjectResearcher:
    def __init__(self, openai_api_key: Optional[str] = None):
        self.openai_api_key = openai_api_key
        if openai_api_key:
            openai.api_key = openai_api_key
        
        self.session = None
        
        # Job categories and their typical indicators
        self.job_indicators = {
            JobCategory.COMMUNITY_MANAGEMENT: {
                'missing_signs': ['inactive discord', 'low engagement', 'unanswered questions', 'no community events'],
                'present_signs': ['active moderators', 'regular ama', 'community challenges', 'active engagement']
            },
            JobCategory.MODERATION: {
                'missing_signs': ['spam messages', 'unmoderated channels', 'inappropriate content', 'no rules'],
                'present_signs': ['clear rules', 'active moderation', 'clean channels', 'organized structure']
            },
            JobCategory.GRAPHICS_DESIGN: {
                'missing_signs': ['poor logo quality', 'inconsistent branding', 'amateur graphics', 'no visual identity'],
                'present_signs': ['professional branding', 'consistent visuals', 'quality graphics', 'brand guidelines']
            },
            JobCategory.SOCIAL_MEDIA: {
                'missing_signs': ['irregular posts', 'low followers', 'poor engagement', 'inactive accounts'],
                'present_signs': ['regular posting', 'growing followers', 'high engagement', 'multi-platform presence']
            },
            JobCategory.PR_MARKETING: {
                'missing_signs': ['no media coverage', 'poor messaging', 'unknown project', 'no press releases'],
                'present_signs': ['media mentions', 'clear messaging', 'press coverage', 'thought leadership']
            },
            JobCategory.BUSINESS_DEVELOPMENT: {
                'missing_signs': ['no partnerships', 'isolated ecosystem', 'no integrations', 'limited network'],
                'present_signs': ['strategic partnerships', 'integrations', 'business relationships', 'ecosystem presence']
            }
        }
        
        # Pitch strategies for different job categories
        self.pitch_strategies = {
            JobCategory.COMMUNITY_MANAGEMENT: {
                'strategy': 'Focus on engagement metrics and community building experience',
                'approach': 'Show examples of communities you\'ve grown and engagement strategies',
                'key_points': ['Community growth track record', 'Engagement strategies', 'Crisis management', 'Event organization']
            },
            JobCategory.MODERATION: {
                'strategy': 'Emphasize reliability, availability, and conflict resolution skills',
                'approach': 'Highlight your availability across time zones and moderation tools experience',
                'key_points': ['24/7 availability', 'Moderation tools expertise', 'Conflict resolution', 'Rule enforcement']
            },
            JobCategory.GRAPHICS_DESIGN: {
                'strategy': 'Lead with a strong portfolio showcasing crypto/web3 design experience',
                'approach': 'Create sample designs specifically for their project before pitching',
                'key_points': ['Crypto design portfolio', 'Brand consistency', 'Quick turnaround', 'Multiple format delivery']
            },
            JobCategory.SOCIAL_MEDIA: {
                'strategy': 'Present a content strategy with growth projections and engagement tactics',
                'approach': 'Analyze their current social media and propose specific improvements',
                'key_points': ['Content strategy', 'Growth tactics', 'Platform expertise', 'Analytics tracking']
            },
            JobCategory.PR_MARKETING: {
                'strategy': 'Demonstrate media connections and successful campaign examples',
                'approach': 'Propose specific PR opportunities and media outreach strategy',
                'key_points': ['Media relationships', 'Campaign success stories', 'Industry knowledge', 'Crisis communication']
            },
            JobCategory.BUSINESS_DEVELOPMENT: {
                'strategy': 'Showcase network connections and partnership facilitation experience',
                'approach': 'Identify potential partnerships and present strategic opportunities',
                'key_points': ['Network connections', 'Deal-making experience', 'Market insights', 'Strategic thinking']
            }
        }
    
    async def init_session(self):
        """Initialize HTTP session for web requests"""
        if not self.session:
            self.session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=30),
                headers={'User-Agent': 'Mozilla/5.0 (compatible; ProjectResearcher/1.0)'}
            )
    
    async def close_session(self):
        """Close HTTP session"""
        if self.session:
            await self.session.close()
    
    async def research_project_comprehensive(self, project_identifier: str) -> ComprehensiveProjectAnalysis:
        """Conduct comprehensive research on a project"""
        await self.init_session()
        
        try:
            # Step 1: Gather basic information
            basic_info = await self.gather_basic_project_info(project_identifier)
            
            # Step 2: Analyze social media presence
            social_analysis = await self.analyze_social_presence(project_identifier, basic_info)
            
            # Step 3: Technical analysis (whitepaper, GitHub, etc.)
            technical_analysis = await self.analyze_technical_aspects(project_identifier, basic_info)
            
            # Step 4: Team analysis
            team_analysis = await self.analyze_team(project_identifier, basic_info)
            
            # Step 5: Community health analysis
            community_analysis = await self.analyze_community_health(project_identifier, basic_info)
            
            # Step 6: Deep dive tokenomics
            tokenomics_analysis = await self.analyze_tokenomics_deep(project_identifier, basic_info)
            
            # Step 7: Identify project needs and job opportunities
            project_needs = await self.identify_project_needs(
                basic_info, social_analysis, technical_analysis, 
                team_analysis, community_analysis
            )
            
            # Step 8: Overall legitimacy analysis
            legitimacy_analysis = await self.create_legitimacy_analysis(
                basic_info, social_analysis, technical_analysis, team_analysis
            )
            
            return ComprehensiveProjectAnalysis(
                project_name=basic_info.get('name', project_identifier),
                project_description=basic_info.get('description', 'No description available'),
                legitimacy_analysis=legitimacy_analysis,
                social_presence=social_analysis,
                technical_analysis=technical_analysis,
                team_analysis=team_analysis,
                community_health=community_analysis,
                tokenomics_deep_dive=tokenomics_analysis,
                project_needs=project_needs,
                research_timestamp=datetime.now(),
                sources_analyzed=basic_info.get('sources', [])
            )
            
        finally:
            await self.close_session()
    
    async def gather_basic_project_info(self, project_identifier: str) -> Dict:
        """Gather basic project information from various sources"""
        project_info = {
            'name': project_identifier,
            'description': '',
            'website': '',
            'social_links': {},
            'sources': []
        }
        
        try:
            # Try to fetch from CoinGecko API
            coingecko_data = await self.fetch_coingecko_data(project_identifier)
            if coingecko_data:
                project_info.update(coingecko_data)
                project_info['sources'].append('CoinGecko')
            
            # Try to fetch from CoinMarketCap (if API available)
            # cmc_data = await self.fetch_coinmarketcap_data(project_identifier)
            
            # Search for project website and social media
            web_search_data = await self.search_project_web_presence(project_identifier)
            if web_search_data:
                project_info.update(web_search_data)
                project_info['sources'].append('Web Search')
            
        except Exception as e:
            logger.error(f"Error gathering basic project info: {e}")
        
        return project_info
    
    async def fetch_coingecko_data(self, project_identifier: str) -> Optional[Dict]:
        """Fetch project data from CoinGecko API"""
        try:
            # Search for the project
            search_url = f"https://api.coingecko.com/api/v3/search?query={project_identifier}"
            async with self.session.get(search_url) as response:
                if response.status == 200:
                    search_data = await response.json()
                    
                    # Find the most relevant result
                    coins = search_data.get('coins', [])
                    if not coins:
                        return None
                    
                    coin = coins[0]  # Take the first match
                    coin_id = coin.get('id')
                    
                    # Get detailed information
                    detail_url = f"https://api.coingecko.com/api/v3/coins/{coin_id}"
                    async with self.session.get(detail_url) as detail_response:
                        if detail_response.status == 200:
                            detail_data = await detail_response.json()
                            
                            return {
                                'name': detail_data.get('name'),
                                'description': detail_data.get('description', {}).get('en', ''),
                                'website': detail_data.get('links', {}).get('homepage', [''])[0],
                                'social_links': {
                                    'twitter': detail_data.get('links', {}).get('twitter_screen_name'),
                                    'telegram': detail_data.get('links', {}).get('telegram_channel_identifier'),
                                    'discord': detail_data.get('links', {}).get('discord'),
                                    'github': detail_data.get('links', {}).get('repos_url', {}).get('github', [])
                                },
                                'market_data': {
                                    'market_cap': detail_data.get('market_data', {}).get('market_cap', {}).get('usd'),
                                    'volume': detail_data.get('market_data', {}).get('total_volume', {}).get('usd'),
                                    'price': detail_data.get('market_data', {}).get('current_price', {}).get('usd')
                                }
                            }
        except Exception as e:
            logger.error(f"CoinGecko API error: {e}")
        
        return None
    
    async def search_project_web_presence(self, project_identifier: str) -> Dict:
        """Search for project's web presence using web search"""
        web_data = {
            'additional_info': '',
            'found_links': []
        }
        
        # This would typically use a search API like Google Custom Search
        # For now, we'll use a placeholder implementation
        search_terms = [
            f"{project_identifier} crypto project",
            f"{project_identifier} whitepaper",
            f"{project_identifier} official website"
        ]
        
        # Placeholder for web search implementation
        # In a real implementation, you'd use Google Custom Search API or similar
        
        return web_data
    
    async def analyze_social_presence(self, project_identifier: str, basic_info: Dict) -> Dict:
        """Analyze project's social media presence"""
        social_analysis = {
            'twitter': {'present': False, 'followers': 0, 'engagement': 'unknown', 'activity': 'unknown'},
            'telegram': {'present': False, 'members': 0, 'activity': 'unknown'},
            'discord': {'present': False, 'members': 0, 'activity': 'unknown'},
            'overall_score': 0,
            'missing_platforms': [],
            'recommendations': []
        }
        
        social_links = basic_info.get('social_links', {})
        
        # Analyze Twitter presence
        if social_links.get('twitter'):
            twitter_analysis = await self.analyze_twitter_account(social_links['twitter'])
            social_analysis['twitter'] = twitter_analysis
        else:
            social_analysis['missing_platforms'].append('twitter')
        
        # Analyze Telegram presence
        if social_links.get('telegram'):
            telegram_analysis = await self.analyze_telegram_channel(social_links['telegram'])
            social_analysis['telegram'] = telegram_analysis
        else:
            social_analysis['missing_platforms'].append('telegram')
        
        # Calculate overall social media score
        social_analysis['overall_score'] = self.calculate_social_media_score(social_analysis)
        
        # Generate recommendations
        social_analysis['recommendations'] = self.generate_social_media_recommendations(social_analysis)
        
        return social_analysis
    
    async def analyze_twitter_account(self, twitter_handle: str) -> Dict:
        """Analyze Twitter account metrics"""
        # Placeholder for Twitter analysis
        # In a real implementation, you'd use Twitter API v2
        return {
            'present': True,
            'followers': 0,  # Would fetch from API
            'engagement': 'unknown',
            'activity': 'unknown',
            'content_quality': 'unknown'
        }
    
    async def analyze_telegram_channel(self, telegram_identifier: str) -> Dict:
        """Analyze Telegram channel/group"""
        # Placeholder for Telegram analysis
        return {
            'present': True,
            'members': 0,
            'activity': 'unknown',
            'moderation_quality': 'unknown'
        }
    
    def calculate_social_media_score(self, social_analysis: Dict) -> int:
        """Calculate overall social media presence score (0-100)"""
        score = 0
        
        # Twitter scoring
        if social_analysis['twitter']['present']:
            score += 30
            followers = social_analysis['twitter']['followers']
            if followers > 10000:
                score += 20
            elif followers > 1000:
                score += 10
        
        # Telegram scoring
        if social_analysis['telegram']['present']:
            score += 25
            members = social_analysis['telegram']['members']
            if members > 5000:
                score += 15
            elif members > 1000:
                score += 8
        
        # Discord scoring
        if social_analysis['discord']['present']:
            score += 25
        
        # Penalty for missing major platforms
        missing_platforms = len(social_analysis['missing_platforms'])
        score -= (missing_platforms * 15)
        
        return max(0, min(100, score))
    
    def generate_social_media_recommendations(self, social_analysis: Dict) -> List[str]:
        """Generate social media improvement recommendations"""
        recommendations = []
        
        if 'twitter' in social_analysis['missing_platforms']:
            recommendations.append("Establish Twitter presence for announcements and community engagement")
        
        if 'telegram' in social_analysis['missing_platforms']:
            recommendations.append("Create Telegram community for real-time discussions")
        
        if 'discord' in social_analysis['missing_platforms']:
            recommendations.append("Set up Discord server for community building and support")
        
        if social_analysis['overall_score'] < 50:
            recommendations.append("Increase social media activity and engagement")
        
        return recommendations
    
    async def analyze_technical_aspects(self, project_identifier: str, basic_info: Dict) -> Dict:
        """Analyze technical aspects of the project"""
        technical_analysis = {
            'whitepaper': {'present': False, 'quality': 'unknown', 'technical_depth': 'unknown'},
            'github': {'present': False, 'activity': 'unknown', 'code_quality': 'unknown'},
            'smart_contracts': {'deployed': False, 'audited': False, 'verified': False},
            'documentation': {'present': False, 'quality': 'unknown'},
            'technical_score': 0,
            'missing_elements': [],
            'recommendations': []
        }
        
        # Check for GitHub presence
        github_repos = basic_info.get('social_links', {}).get('github', [])
        if github_repos:
            github_analysis = await self.analyze_github_presence(github_repos)
            technical_analysis['github'] = github_analysis
        else:
            technical_analysis['missing_elements'].append('github_repository')
        
        # Check for whitepaper
        website = basic_info.get('website', '')
        if website:
            whitepaper_analysis = await self.check_whitepaper_presence(website)
            technical_analysis['whitepaper'] = whitepaper_analysis
        else:
            technical_analysis['missing_elements'].append('whitepaper')
        
        # Generate technical score and recommendations
        technical_analysis['technical_score'] = self.calculate_technical_score(technical_analysis)
        technical_analysis['recommendations'] = self.generate_technical_recommendations(technical_analysis)
        
        return technical_analysis
    
    async def analyze_github_presence(self, github_repos: List[str]) -> Dict:
        """Analyze GitHub repository presence and activity"""
        # Placeholder for GitHub API analysis
        return {
            'present': len(github_repos) > 0,
            'repo_count': len(github_repos),
            'activity': 'unknown',  # Would analyze commits, issues, etc.
            'code_quality': 'unknown',
            'last_update': 'unknown'
        }
    
    async def check_whitepaper_presence(self, website: str) -> Dict:
        """Check for whitepaper presence and quality"""
        # Placeholder for whitepaper analysis
        return {
            'present': False,  # Would search website for whitepaper links
            'quality': 'unknown',
            'technical_depth': 'unknown',
            'readability': 'unknown'
        }
    
    def calculate_technical_score(self, technical_analysis: Dict) -> int:
        """Calculate technical maturity score"""
        score = 0
        
        if technical_analysis['github']['present']:
            score += 40
        if technical_analysis['whitepaper']['present']:
            score += 30
        if technical_analysis['smart_contracts']['deployed']:
            score += 20
        if technical_analysis['smart_contracts']['audited']:
            score += 10
        
        # Penalty for missing critical elements
        missing_count = len(technical_analysis['missing_elements'])
        score -= (missing_count * 20)
        
        return max(0, min(100, score))
    
    def generate_technical_recommendations(self, technical_analysis: Dict) -> List[str]:
        """Generate technical improvement recommendations"""
        recommendations = []
        
        if 'github_repository' in technical_analysis['missing_elements']:
            recommendations.append("Create public GitHub repository to showcase development progress")
        
        if 'whitepaper' in technical_analysis['missing_elements']:
            recommendations.append("Publish detailed whitepaper explaining technology and tokenomics")
        
        if not technical_analysis['smart_contracts']['audited']:
            recommendations.append("Get smart contracts professionally audited for security")
        
        return recommendations
    
    async def analyze_team(self, project_identifier: str, basic_info: Dict) -> Dict:
        """Analyze project team transparency and credentials"""
        team_analysis = {
            'transparency': 'unknown',  # 'high', 'medium', 'low', 'anonymous'
            'team_size': 'unknown',
            'experience': 'unknown',
            'linkedin_profiles': 0,
            'public_backgrounds': 0,
            'team_score': 0,
            'missing_elements': [],
            'recommendations': []
        }
        
        # This would typically analyze team page on website, LinkedIn profiles, etc.
        # Placeholder implementation
        
        description = basic_info.get('description', '')
        website = basic_info.get('website', '')
        
        # Look for team-related keywords in description
        team_keywords = ['team', 'founder', 'ceo', 'developer', 'advisor']
        team_mentions = sum(1 for keyword in team_keywords if keyword in description.lower())
        
        if team_mentions == 0:
            team_analysis['missing_elements'].append('team_information')
            team_analysis['transparency'] = 'anonymous'
        elif team_mentions < 3:
            team_analysis['transparency'] = 'low'
        else:
            team_analysis['transparency'] = 'medium'
        
        team_analysis['team_score'] = self.calculate_team_score(team_analysis)
        team_analysis['recommendations'] = self.generate_team_recommendations(team_analysis)
        
        return team_analysis
    
    def calculate_team_score(self, team_analysis: Dict) -> int:
        """Calculate team transparency score"""
        score = 0
        
        transparency = team_analysis['transparency']
        if transparency == 'high':
            score += 50
        elif transparency == 'medium':
            score += 30
        elif transparency == 'low':
            score += 10
        # anonymous = 0 points
        
        score += team_analysis['linkedin_profiles'] * 10
        score += team_analysis['public_backgrounds'] * 5
        
        return min(100, score)
    
    def generate_team_recommendations(self, team_analysis: Dict) -> List[str]:
        """Generate team-related recommendations"""
        recommendations = []
        
        if team_analysis['transparency'] == 'anonymous':
            recommendations.append("Consider revealing team members to build trust and credibility")
        elif team_analysis['transparency'] == 'low':
            recommendations.append("Provide more detailed team information and backgrounds")
        
        if team_analysis['linkedin_profiles'] == 0:
            recommendations.append("Create professional LinkedIn profiles for team members")
        
        return recommendations
    
    async def analyze_community_health(self, project_identifier: str, basic_info: Dict) -> Dict:
        """Analyze community health and engagement"""
        community_analysis = {
            'size': 'unknown',
            'engagement_rate': 'unknown',
            'growth_trend': 'unknown',
            'community_sentiment': 'neutral',
            'moderation_quality': 'unknown',
            'community_score': 0,
            'issues': [],
            'recommendations': []
        }
        
        # This would analyze community metrics across platforms
        # Placeholder implementation
        
        community_analysis['community_score'] = self.calculate_community_score(community_analysis)
        community_analysis['recommendations'] = self.generate_community_recommendations(community_analysis)
        
        return community_analysis
    
    def calculate_community_score(self, community_analysis: Dict) -> int:
        """Calculate community health score"""
        # Placeholder scoring logic
        return 50  # Default neutral score
    
    def generate_community_recommendations(self, community_analysis: Dict) -> List[str]:
        """Generate community improvement recommendations"""
        return ["Increase community engagement through regular events and updates"]
    
    async def analyze_tokenomics_deep(self, project_identifier: str, basic_info: Dict) -> Dict:
        """Deep dive tokenomics analysis"""
        tokenomics_analysis = {
            'token_supply': 'unknown',
            'distribution': 'unknown',
            'utility': 'unknown',
            'inflation_mechanism': 'unknown',
            'burn_mechanism': False,
            'staking': False,
            'governance': False,
            'tokenomics_score': 0,
            'red_flags': [],
            'positive_aspects': [],
            'recommendations': []
        }
        
        description = basic_info.get('description', '')
        
        # Analyze tokenomics from description
        if 'unlimited supply' in description.lower():
            tokenomics_analysis['red_flags'].append('unlimited_supply')
        
        if 'burn' in description.lower():
            tokenomics_analysis['burn_mechanism'] = True
            tokenomics_analysis['positive_aspects'].append('burn_mechanism')
        
        if 'staking' in description.lower():
            tokenomics_analysis['staking'] = True
            tokenomics_analysis['positive_aspects'].append('staking_utility')
        
        if 'governance' in description.lower():
            tokenomics_analysis['governance'] = True
            tokenomics_analysis['positive_aspects'].append('governance_utility')
        
        tokenomics_analysis['tokenomics_score'] = self.calculate_tokenomics_score(tokenomics_analysis)
        tokenomics_analysis['recommendations'] = self.generate_tokenomics_recommendations(tokenomics_analysis)
        
        return tokenomics_analysis
    
    def calculate_tokenomics_score(self, tokenomics_analysis: Dict) -> int:
        """Calculate tokenomics quality score"""
        score = 50  # Base score
        
        # Add points for positive aspects
        score += len(tokenomics_analysis['positive_aspects']) * 15
        
        # Subtract points for red flags
        score -= len(tokenomics_analysis['red_flags']) * 25
        
        return max(0, min(100, score))
    
    def generate_tokenomics_recommendations(self, tokenomics_analysis: Dict) -> List[str]:
        """Generate tokenomics improvement recommendations"""
        recommendations = []
        
        if not tokenomics_analysis['burn_mechanism']:
            recommendations.append("Consider implementing token burn mechanism for deflationary pressure")
        
        if not tokenomics_analysis['staking']:
            recommendations.append("Add staking utility to encourage long-term holding")
        
        if not tokenomics_analysis['governance']:
            recommendations.append("Implement governance functionality for community participation")
        
        return recommendations
    
    async def identify_project_needs(self, basic_info: Dict, social_analysis: Dict, 
                                   technical_analysis: Dict, team_analysis: Dict, 
                                   community_analysis: Dict) -> ProjectNeeds:
        """Identify project needs and job opportunities"""
        
        missing_elements = []
        strengths = []
        improvement_areas = []
        job_opportunities = []
        
        # Analyze social media needs
        if social_analysis['overall_score'] < 70:
            missing_elements.append("strong_social_media_presence")
            improvement_areas.append("social_media_strategy")
            
            # Check specific platforms for job opportunities
            if 'twitter' in social_analysis['missing_platforms']:
                job_opportunities.append(self.create_job_opportunity(
                    JobCategory.SOCIAL_MEDIA, "high",
                    "Twitter account management and content strategy needed",
                    ["Social media experience", "Crypto knowledge", "Content creation"],
                    self.pitch_strategies[JobCategory.SOCIAL_MEDIA],
                    "$500-2000/month", "Part-time (10-20 hrs/week)"
                ))
            
            if social_analysis['telegram'].get('members', 0) < 1000:
                job_opportunities.append(self.create_job_opportunity(
                    JobCategory.COMMUNITY_MANAGEMENT, "high",
                    "Telegram community growth and management needed",
                    ["Community building experience", "24/7 availability", "Crypto enthusiasm"],
                    self.pitch_strategies[JobCategory.COMMUNITY_MANAGEMENT],
                    "$800-3000/month", "Full-time"
                ))
        
        # Analyze technical needs
        if technical_analysis['technical_score'] < 60:
            missing_elements.append("strong_technical_foundation")
            improvement_areas.append("technical_documentation")
            
            if 'whitepaper' in technical_analysis['missing_elements']:
                job_opportunities.append(self.create_job_opportunity(
                    JobCategory.TECHNICAL_WRITING, "high",
                    "Technical writer needed for whitepaper and documentation",
                    ["Technical writing experience", "Blockchain knowledge", "Research skills"],
                    self.pitch_strategies.get(JobCategory.TECHNICAL_WRITING, {}),
                    "$2000-8000 (one-time)", "Project-based"
                ))
            
            if 'github_repository' in technical_analysis['missing_elements']:
                job_opportunities.append(self.create_job_opportunity(
                    JobCategory.DEVELOPMENT, "medium",
                    "Blockchain developer needed for smart contract development",
                    ["Solidity experience", "Smart contract development", "Security knowledge"],
                    self.pitch_strategies.get(JobCategory.DEVELOPMENT, {}),
                    "$3000-10000/month", "Full-time"
                ))
        
        # Analyze team transparency needs
        if team_analysis['team_score'] < 50:
            missing_elements.append("team_transparency")
            improvement_areas.append("team_credibility")
            
            job_opportunities.append(self.create_job_opportunity(
                JobCategory.PR_MARKETING, "medium",
                "PR specialist needed to build team credibility and media presence",
                ["PR experience", "Media relationships", "Crisis communication"],
                self.pitch_strategies[JobCategory.PR_MARKETING],
                "$1500-5000/month", "Part-time"
            ))
        
        # Check for graphics/design needs
        if not self.has_professional_branding(basic_info, social_analysis):
            missing_elements.append("professional_branding")
            improvement_areas.append("visual_identity")
            
            job_opportunities.append(self.create_job_opportunity(
                JobCategory.GRAPHICS_DESIGN, "medium",
                "Graphics designer needed for branding and visual content",
                ["Graphic design portfolio", "Crypto/Web3 experience", "Brand development"],
                self.pitch_strategies[JobCategory.GRAPHICS_DESIGN],
                "$1000-4000/month", "Part-time"
            ))
        
        # Check for business development needs
        market_cap = basic_info.get('market_data', {}).get('market_cap', 0)
        if market_cap < 10000000:  # Less than $10M market cap
            missing_elements.append("strategic_partnerships")
            improvement_areas.append("business_development")
            
            job_opportunities.append(self.create_job_opportunity(
                JobCategory.BUSINESS_DEVELOPMENT, "medium",
                "Business development specialist for partnerships and growth",
                ["BD experience", "Crypto industry network", "Deal-making skills"],
                self.pitch_strategies[JobCategory.BUSINESS_DEVELOPMENT],
                "$2000-8000/month", "Part-time to Full-time"
            ))
        
        # Identify strengths
        if social_analysis['overall_score'] > 70:
            strengths.append("strong_social_media_presence")
        if technical_analysis['technical_score'] > 70:
            strengths.append("solid_technical_foundation")
        if team_analysis['team_score'] > 70:
            strengths.append("transparent_team")
        
        # Determine overall maturity
        avg_score = (social_analysis['overall_score'] + technical_analysis['technical_score'] + 
                    team_analysis['team_score']) / 3
        
        if avg_score < 40:
            overall_maturity = "early"
        elif avg_score < 70:
            overall_maturity = "developing"
        else:
            overall_maturity = "mature"
        
        return ProjectNeeds(
            missing_elements=missing_elements,
            strengths=strengths,
            improvement_areas=improvement_areas,
            job_opportunities=job_opportunities,
            overall_maturity=overall_maturity
        )
    
    def create_job_opportunity(self, category: JobCategory, urgency: str, description: str,
                             requirements: List[str], pitch_strategy: Dict, 
                             estimated_budget: str, time_commitment: str) -> JobOpportunity:
        """Create a job opportunity with pitch guidance"""
        return JobOpportunity(
            category=category,
            urgency=urgency,
            description=description,
            requirements=requirements,
            pitch_strategy=self.format_pitch_strategy(pitch_strategy, category),
            estimated_budget=estimated_budget,
            time_commitment=time_commitment
        )
    
    def format_pitch_strategy(self, strategy_dict: Dict, category: JobCategory) -> str:
        """Format pitch strategy into actionable guidance"""
        if not strategy_dict:
            return "Research the project thoroughly and propose specific improvements in your area of expertise."
        
        strategy = strategy_dict.get('strategy', '')
        approach = strategy_dict.get('approach', '')
        key_points = strategy_dict.get('key_points', [])
        
        formatted_strategy = f"""
**Pitch Strategy:** {strategy}

**Approach:** {approach}

**Key Points to Highlight:**
{chr(10).join([f'• {point}' for point in key_points])}

**Pitch Template:**
"Hi [Project Name] team! I've been following your project and see great potential. I noticed you could benefit from {category.value.replace('_', ' ')} support. Here's how I can help:

[Specific examples of what you can deliver]
[Your relevant experience/portfolio]
[Proposed timeline and deliverables]

I'd love to discuss how we can grow [Project Name] together. When would be a good time for a brief call?"
        """
        
        return formatted_strategy.strip()
    
    def has_professional_branding(self, basic_info: Dict, social_analysis: Dict) -> bool:
        """Check if project has professional branding"""
        # This would typically analyze logo quality, brand consistency, etc.
        # Simplified check for demo
        return False  # Assume most projects need branding help
    
    async def create_legitimacy_analysis(self, basic_info: Dict, social_analysis: Dict,
                                       technical_analysis: Dict, team_analysis: Dict) -> ProjectAnalysis:
        """Create overall legitimacy analysis"""
        
        # Collect indicators
        scam_indicators = []
        positive_indicators = []
        
        # Analyze based on gathered data
        if team_analysis['transparency'] == 'anonymous':
            scam_indicators.append("MEDIUM RISK: Anonymous team")
        else:
            positive_indicators.append("POSITIVE: Team information available")
        
        if technical_analysis['technical_score'] < 30:
            scam_indicators.append("HIGH RISK: Poor technical foundation")
        elif technical_analysis['technical_score'] > 70:
            positive_indicators.append("POSITIVE: Strong technical foundation")
        
        if social_analysis['overall_score'] < 20:
            scam_indicators.append("MEDIUM RISK: Minimal social media presence")
        elif social_analysis['overall_score'] > 60:
            positive_indicators.append("POSITIVE: Good social media presence")
        
        # Calculate overall legitimacy score
        scores = [
            social_analysis['overall_score'],
            technical_analysis['technical_score'],
            team_analysis['team_score']
        ]
        legitimacy_score = sum(scores) / len(scores)
        
        # Determine risk level
        if legitimacy_score > 70:
            risk_level = ScamRisk.LOW
        elif legitimacy_score > 50:
            risk_level = ScamRisk.MEDIUM
        elif legitimacy_score > 30:
            risk_level = ScamRisk.HIGH
        else:
            risk_level = ScamRisk.CRITICAL
        
        return ProjectAnalysis(
            legitimacy_score=legitimacy_score,
            scam_indicators=scam_indicators,
            positive_indicators=positive_indicators,
            risk_level=risk_level,
            tokenomics_analysis="See detailed tokenomics analysis",
            roadmap_quality="See technical analysis",
            team_analysis="See team analysis",
            sentiment_score=0.0  # Would calculate from community sentiment
        )import asyncio
import aiohttp
import json
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Set, Optional, Tuple
import re
import sqlite3
from dataclasses import dataclass
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from telethon import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, Channel, Chat
import feedparser
import os
from bs4 import BeautifulSoup
import hashlib
import tweepy
from enum import Enum
import openai
from textstat import flesch_reading_ease
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import requests
from urllib.parse import urlparse
import time

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Download required NLTK data
try:
    nltk.download('vader_lexicon', quiet=True)
except:
    logger.warning("Could not download NLTK data - sentiment analysis may not work")

class ProjectStage(Enum):
    PRE_SEED = "pre_seed"
    SEED = "seed"
    SERIES_A = "series_a"
    SERIES_B = "series_b"
    ICO_IDO = "ico_ido"
    STARTUP = "startup"
    SMALL_COMMUNITY = "small_community"
    NEWLY_LAUNCHED = "newly_launched"
    TELEGRAM_COMMUNITY = "telegram_community"

class CommunitySize(Enum):
    MICRO = "1-30"
    SMALL = "31-50" 
    MEDIUM_SMALL = "51-100"
    MEDIUM = "101-200"
    GROWING = "201-500"

class JobCategory(Enum):
    COMMUNITY_MANAGEMENT = "community_management"
    MODERATION = "moderation"
    GRAPHICS_DESIGN = "graphics_design"
    SOCIAL_MEDIA = "social_media"
    PR_MARKETING = "pr_marketing"
    BUSINESS_DEVELOPMENT = "business_development"
    TECHNICAL_WRITING = "technical_writing"
    DEVELOPMENT = "development"
    LEGAL_COMPLIANCE = "legal_compliance"
    PARTNERSHIPS = "partnerships"
    CONTENT_CREATION = "content_creation"
    INFLUENCER_OUTREACH = "influencer_outreach"

@dataclass
class JobOpportunity:
    category: JobCategory
    urgency: str  # "high", "medium", "low"
    description: str
    requirements: List[str]
    pitch_strategy: str
    estimated_budget: str
    time_commitment: str

@dataclass
class ProjectNeeds:
    missing_elements: List[str]
    strengths: List[str]
    improvement_areas: List[str]
    job_opportunities: List[JobOpportunity]
    overall_maturity: str  # "early", "developing", "mature"

@dataclass
class ComprehensiveProjectAnalysis:
    project_name: str
    project_description: str
    legitimacy_analysis: ProjectAnalysis
    social_presence: Dict[str, any]
    technical_analysis: Dict[str, any]
    team_analysis: Dict[str, any]
    community_health: Dict[str, any]
    tokenomics_deep_dive: Dict[str, any]
    project_needs: ProjectNeeds
    research_timestamp: datetime
    sources_analyzed: List[str]

@dataclass
class TelegramCommunityInfo:
    title: str
    username: str
    member_count: int
    description: str
    recent_messages: List[str]
    admin_count: int
    creation_date: Optional[datetime]
    invite_link: Optional[str]
    category: str
    verified: bool
    restricted: bool

@dataclass
class ProjectAnalysis:
    legitimacy_score: float  # 0-100
    scam_indicators: List[str]
    positive_indicators: List[str]
    risk_level: ScamRisk
    tokenomics_analysis: Optional[str]
    roadmap_quality: Optional[str]
    team_analysis: Optional[str]
    sentiment_score: float

@dataclass
class CommunityAlert:
    community_info: TelegramCommunityInfo
    project_analysis: ProjectAnalysis
    discovery_timestamp: datetime
    unique_id: str
    size_category: CommunitySize

class TelegramScout:
    def __init__(self, api_id: int, api_hash: str, phone_number: str, session_name: str = "scout_session"):
        self.api_id = api_id
        self.api_hash = api_hash
        self.phone_number = phone_number
        self.session_name = session_name
        self.client = None
        
        # Web3/Crypto related keywords for community detection
        self.crypto_keywords = [
            'defi', 'nft', 'dao', 'web3', 'crypto', 'blockchain', 'token', 'coin',
            'dapp', 'protocol', 'yield', 'farming', 'staking', 'metaverse', 'gamefi',
            'bridge', 'swap', 'dex', 'cex', 'mining', 'node', 'validator',
            'ethereum', 'bitcoin', 'solana', 'polygon', 'avalanche', 'bsc'
        ]
        
        # Scam indicators
        self.scam_indicators = {
            'high_risk': [
                'guaranteed profit', 'risk-free', '100% safe', 'get rich quick',
                'urgent', 'limited time', 'exclusive opportunity', 'secret method',
                'financial freedom', 'millionaire', 'lamborghini', 'to the moon',
                'pump', 'dump', 'shill', 'exit scam', 'rug pull'
            ],
            'medium_risk': [
                'investment opportunity', 'high returns', 'passive income',
                'early investor', 'presale', 'private sale', 'airdrop',
                'referral bonus', 'pyramid', 'matrix', 'doubler'
            ],
            'suspicious_patterns': [
                r'\d+x profit', r'\d+% return', r'\$\d+k per', r'only \d+ spots',
                r'invest \$\d+ get \$\d+', r'\d+ btc', r'\d+ eth'
            ]
        }
        
        # Legitimacy indicators
        self.legitimacy_indicators = {
            'positive': [
                'whitepaper', 'roadmap', 'github', 'audit', 'doxxed team',
                'partnership', 'testnet', 'mainnet', 'smart contract',
                'open source', 'decentralized', 'community driven',
                'development update', 'milestone', 'alpha', 'beta'
            ],
            'team_indicators': [
                'founder', 'ceo', 'cto', 'developer', 'advisor',
                'team member', 'linkedin', 'experience', 'background'
            ],
            'tech_indicators': [
                'consensus', 'validator', 'node', 'blockchain', 'protocol',
                'algorithm', 'cryptography', 'security', 'scalability'
            ]
        }
    
    async def initialize(self):
        """Initialize Telegram client"""
        self.client = TelegramClient(self.session_name, self.api_id, self.api_hash)
        await self.client.start(phone=self.phone_number)
        logger.info("Telegram client initialized")
    
    async def close(self):
        """Close Telegram client"""
        if self.client:
            await self.client.disconnect()
    
    async def search_crypto_communities(self, size_filters: List[CommunitySize]) -> List[TelegramCommunityInfo]:
        """Search for crypto communities within specified size ranges"""
        if not self.client:
            await self.initialize()
        
        communities = []
        offset_peer = InputPeerEmpty()
        
        try:
            # Get dialogs (chats/channels the account is part of)
            result = await self.client(GetDialogsRequest(
                offset_date=None,
                offset_id=0,
                offset_peer=offset_peer,
                limit=200,
                hash=0
            ))
            
            for chat in result.chats:
                if isinstance(chat, (Channel, Chat)):
                    # Check if it's a crypto-related community
                    if await self.is_crypto_community(chat):
                        community_info = await self.get_community_info(chat)
                        
                        # Filter by size
                        if self.matches_size_filter(community_info.member_count, size_filters):
                            communities.append(community_info)
            
            # Additionally search for public communities using search
            search_results = await self.search_public_communities()
            for community in search_results:
                if self.matches_size_filter(community.member_count, size_filters):
                    communities.append(community)
            
        except Exception as e:
            logger.error(f"Error searching communities: {e}")
        
        return communities
    
    async def is_crypto_community(self, chat) -> bool:
        """Check if a chat/channel is crypto-related"""
        try:
            title = getattr(chat, 'title', '').lower()
            description = ''
            
            # Get more detailed info if it's a channel
            if hasattr(chat, 'username') and chat.username:
                try:
                    entity = await self.client.get_entity(chat.username)
                    if hasattr(entity, 'about'):
                        description = entity.about.lower()
                except:
                    pass
            
            text_to_check = f"{title} {description}"
            return any(keyword in text_to_check for keyword in self.crypto_keywords)
        except Exception as e:
            logger.error(f"Error checking if crypto community: {e}")
            return False
    
    async def get_community_info(self, chat) -> TelegramCommunityInfo:
        """Get detailed information about a community"""
        try:
            title = getattr(chat, 'title', 'Unknown')
            username = getattr(chat, 'username', None)
            member_count = getattr(chat, 'participants_count', 0)
            
            # Get recent messages for analysis
            recent_messages = await self.get_recent_messages(chat)
            
            # Get admin count
            admin_count = await self.get_admin_count(chat)
            
            # Get creation date
            creation_date = getattr(chat, 'date', None)
            
            # Generate invite link if possible
            invite_link = None
            if username:
                invite_link = f"https://t.me/{username}"
            
            # Get description
            description = ""
            try:
                if hasattr(chat, 'username') and chat.username:
                    entity = await self.client.get_entity(chat.username)
                    if hasattr(entity, 'about'):
                        description = entity.about
            except:
                pass
            
            return TelegramCommunityInfo(
                title=title,
                username=username or "",
                member_count=member_count,
                description=description,
                recent_messages=recent_messages,
                admin_count=admin_count,
                creation_date=creation_date,
                invite_link=invite_link,
                category="crypto",
                verified=getattr(chat, 'verified', False),
                restricted=getattr(chat, 'restricted', False)
            )
            
        except Exception as e:
            logger.error(f"Error getting community info: {e}")
            return None
    
    async def get_recent_messages(self, chat, limit: int = 50) -> List[str]:
        """Get recent messages from a chat for analysis"""
        messages = []
        try:
            async for message in self.client.iter_messages(chat, limit=limit):
                if message.text:
                    messages.append(message.text[:500])  # Limit message length
        except Exception as e:
            logger.error(f"Error getting recent messages: {e}")
        
        return messages
    
    async def get_admin_count(self, chat) -> int:
        """Get number of administrators"""
        try:
            participants = await self.client.get_participants(chat, filter=None)
            admin_count = sum(1 for p in participants if hasattr(p.participant, 'admin_rights'))
            return admin_count
        except:
            return 0
    
    async def search_public_communities(self) -> List[TelegramCommunityInfo]:
        """Search for public crypto communities"""
        communities = []
        search_terms = ['crypto', 'defi', 'nft', 'web3', 'blockchain']
        
        try:
            for term in search_terms:
                try:
                    results = await self.client.get_dialogs(limit=20)
                    # This is a simplified approach - actual public search is more complex
                    # and requires special permissions or using the search functionality
                    break
                except Exception as e:
                    logger.debug(f"Search error for {term}: {e}")
                    continue
        except Exception as e:
            logger.error(f"Error in public community search: {e}")
        
        return communities
    
    def matches_size_filter(self, member_count: int, size_filters: List[CommunitySize]) -> bool:
        """Check if community size matches filter criteria"""
        for size_filter in size_filters:
            if size_filter == CommunitySize.MICRO and 1 <= member_count <= 30:
                return True
            elif size_filter == CommunitySize.SMALL and 31 <= member_count <= 50:
                return True
            elif size_filter == CommunitySize.MEDIUM_SMALL and 51 <= member_count <= 100:
                return True
            elif size_filter == CommunitySize.MEDIUM and 101 <= member_count <= 200:
                return True
            elif size_filter == CommunitySize.GROWING and 201 <= member_count <= 500:
                return True
        return False

class ProjectAnalyzer:
    def __init__(self, openai_api_key: Optional[str] = None):
        self.openai_api_key = openai_api_key
        if openai_api_key:
            openai.api_key = openai_api_key
        
        try:
            self.sentiment_analyzer = SentimentIntensityAnalyzer()
        except:
            self.sentiment_analyzer = None
            logger.warning("Sentiment analyzer not available")
    
    async def analyze_project(self, community_info: TelegramCommunityInfo) -> ProjectAnalysis:
        """Comprehensive project analysis"""
        
        # Combine all text for analysis
        all_text = f"{community_info.title} {community_info.description} " + \
                  " ".join(community_info.recent_messages[:10])
        
        # Basic scam detection
        scam_indicators = self.detect_scam_indicators(all_text)
        positive_indicators = self.detect_positive_indicators(all_text)
        
        # Calculate legitimacy score
        legitimacy_score = self.calculate_legitimacy_score(
            scam_indicators, positive_indicators, community_info
        )
        
        # Determine risk level
        risk_level = self.determine_risk_level(legitimacy_score, scam_indicators)
        
        # Analyze specific aspects
        tokenomics_analysis = await self.analyze_tokenomics(all_text)
        roadmap_quality = self.analyze_roadmap_quality(all_text)
        team_analysis = self.analyze_team_presence(all_text)
        
        # Sentiment analysis
        sentiment_score = self.analyze_sentiment(all_text)
        
        return ProjectAnalysis(
            legitimacy_score=legitimacy_score,
            scam_indicators=scam_indicators,
            positive_indicators=positive_indicators,
            risk_level=risk_level,
            tokenomics_analysis=tokenomics_analysis,
            roadmap_quality=roadmap_quality,
            team_analysis=team_analysis,
            sentiment_score=sentiment_score
        )
    
    def detect_scam_indicators(self, text: str) -> List[str]:
        """Detect potential scam indicators in text"""
        indicators = []
        text_lower = text.lower()
        
        # High risk indicators
        for indicator in self.scout.scam_indicators['high_risk']:
            if indicator in text_lower:
                indicators.append(f"HIGH RISK: {indicator}")
        
        # Medium risk indicators
        for indicator in self.scout.scam_indicators['medium_risk']:
            if indicator in text_lower:
                indicators.append(f"MEDIUM RISK: {indicator}")
        
        # Pattern matching
        for pattern in self.scout.scam_indicators['suspicious_patterns']:
            matches = re.findall(pattern, text_lower)
            for match in matches:
                indicators.append(f"SUSPICIOUS PATTERN: {match}")
        
        # Additional heuristics
        if len(re.findall(r'[🚀💰💎🔥⚡]', text)) > 10:
            indicators.append("EXCESSIVE HYPE EMOJIS")
        
        if 'telegram.me' in text_lower or 't.me' in text_lower:
            # Count suspicious links
            suspicious_links = len(re.findall(r't\.me/[a-zA-Z0-9_]+', text_lower))
            if suspicious_links > 3:
                indicators.append("MULTIPLE SUSPICIOUS LINKS")
        
        return indicators
    
    def detect_positive_indicators(self, text: str) -> List[str]:
        """Detect positive legitimacy indicators"""
        indicators = []
        text_lower = text.lower()
        
        # Positive indicators
        for indicator in self.scout.legitimacy_indicators['positive']:
            if indicator in text_lower:
                indicators.append(f"POSITIVE: {indicator}")
        
        # Team indicators
        for indicator in self.scout.legitimacy_indicators['team_indicators']:
            if indicator in text_lower:
                indicators.append(f"TEAM: {indicator}")
        
        # Technical indicators
        for indicator in self.scout.legitimacy_indicators['tech_indicators']:
            if indicator in text_lower:
                indicators.append(f"TECHNICAL: {indicator}")
        
        # Additional positive signs
        if 'github.com' in text_lower:
            indicators.append("GITHUB REPOSITORY")
        
        if any(word in text_lower for word in ['audit', 'certik', 'peckshield']):
            indicators.append("SECURITY AUDIT")
        
        if 'whitepaper' in text_lower or 'lite paper' in text_lower:
            indicators.append("DOCUMENTATION")
        
        return indicators
    
    def calculate_legitimacy_score(self, scam_indicators: List[str], 
                                 positive_indicators: List[str],
                                 community_info: TelegramCommunityInfo) -> float:
        """Calculate overall legitimacy score (0-100)"""
        base_score = 50.0
        
        # Subtract for scam indicators
        high_risk_count = len([i for i in scam_indicators if 'HIGH RISK' in i])
        medium_risk_count = len([i for i in scam_indicators if 'MEDIUM RISK' in i])
        suspicious_patterns = len([i for i in scam_indicators if 'SUSPICIOUS PATTERN' in i])
        
        base_score -= (high_risk_count * 20)
        base_score -= (medium_risk_count * 10)
        base_score -= (suspicious_patterns * 5)
        
        # Add for positive indicators
        positive_count = len([i for i in positive_indicators if 'POSITIVE' in i])
        team_count = len([i for i in positive_indicators if 'TEAM' in i])
        tech_count = len([i for i in positive_indicators if 'TECHNICAL' in i])
        
        base_score += (positive_count * 8)
        base_score += (team_count * 12)
        base_score += (tech_count * 10)
        
        # Community factors
        if community_info.admin_count > 1:
            base_score += 5
        
        if community_info.verified:
            base_score += 15
        
        if community_info.restricted:
            base_score -= 10
        
        # Age factor
        if community_info.creation_date:
            days_old = (datetime.now() - community_info.creation_date.replace(tzinfo=None)).days
            if days_old > 30:
                base_score += min(10, days_old / 10)
        
        return max(0, min(100, base_score))
    
    def determine_risk_level(self, legitimacy_score: float, scam_indicators: List[str]) -> ScamRisk:
        """Determine overall risk level"""
        high_risk_count = len([i for i in scam_indicators if 'HIGH RISK' in i])
        
        if high_risk_count > 0 or legitimacy_score < 20:
            return ScamRisk.CRITICAL
        elif legitimacy_score < 40:
            return ScamRisk.HIGH
        elif legitimacy_score < 60:
            return ScamRisk.MEDIUM
        else:
            return ScamRisk.LOW
    
    async def analyze_tokenomics(self, text: str) -> Optional[str]:
        """Analyze tokenomics quality using AI if available"""
        if not self.openai_api_key:
            return self.basic_tokenomics_analysis(text)
        
        try:
            prompt = f"""
            Analyze the tokenomics of this crypto project based on the following text:
            
            {text[:2000]}
            
            Evaluate:
            1. Token distribution fairness
            2. Utility and purpose
            3. Inflation/deflation mechanisms
            4. Vesting schedules
            5. Overall sustainability
            
            Provide a brief assessment (max 200 words):
            """
            
            response = await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=200,
                temperature=0.3
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"AI tokenomics analysis failed: {e}")
            return self.basic_tokenomics_analysis(text)
    
    def basic_tokenomics_analysis(self, text: str) -> str:
        """Basic tokenomics analysis without AI"""
        text_lower = text.lower()
        
        analysis = []
        
        if 'token' in text_lower:
            analysis.append("Token mentioned")
        if 'supply' in text_lower:
            analysis.append("Supply information present")
        if 'burn' in text_lower or 'deflationary' in text_lower:
            analysis.append("Deflationary mechanism")
        if 'stake' in text_lower or 'staking' in text_lower:
            analysis.append("Staking utility")
        if 'governance' in text_lower:
            analysis.append("Governance utility")
        
        # Red flags
        if 'unlimited supply' in text_lower:
            analysis.append("⚠️ Unlimited supply")
        if 'dev wallet' in text_lower and '90%' in text_lower:
            analysis.append("⚠️ High dev allocation")
        
        return "; ".join(analysis) if analysis else "Limited tokenomics information"
    
    def analyze_roadmap_quality(self, text: str) -> str:
        """Analyze roadmap quality"""
        text_lower = text.lower()
        
        quality_indicators = []
        
        if 'roadmap' in text_lower:
            quality_indicators.append("Roadmap present")
        if 'q1' in text_lower or 'q2' in text_lower or 'quarter' in text_lower:
            quality_indicators.append("Quarterly planning")
        if 'milestone' in text_lower:
            quality_indicators.append("Clear milestones")
        if 'phase' in text_lower:
            quality_indicators.append("Phased development")
        if 'mainnet' in text_lower or 'testnet' in text_lower:
            quality_indicators.append("Network deployment planned")
        
        # Red flags
        if 'moon' in text_lower or 'lambo' in text_lower:
            quality_indicators.append("⚠️ Unrealistic expectations")
        if 'coming soon' in text_lower and len(quality_indicators) == 0:
            quality_indicators.append("⚠️ Vague timeline")
        
        return "; ".join(quality_indicators) if quality_indicators else "No roadmap information"
    
    def analyze_team_presence(self, text: str) -> str:
        """Analyze team presence and transparency"""
        text_lower = text.lower()
        
        team_indicators = []
        
        if 'team' in text_lower:
            team_indicators.append("Team mentioned")
        if 'founder' in text_lower or 'ceo' in text_lower:
            team_indicators.append("Leadership identified")
        if 'doxxed' in text_lower:
            team_indicators.append("Doxxed team")
        if 'anonymous' in text_lower:
            team_indicators.append("⚠️ Anonymous team")
        if 'linkedin' in text_lower:
            team_indicators.append("Professional profiles")
        if 'experience' in text_lower or 'background' in text_lower:
            team_indicators.append("Experience highlighted")
        
        return "; ".join(team_indicators) if team_indicators else "Limited team information"
    
    def analyze_sentiment(self, text: str) -> float:
        """Analyze overall sentiment of project communications"""
        if not self.sentiment_analyzer:
            return 0.0
        
        try:
            scores = self.sentiment_analyzer.polarity_scores(text)
            return scores['compound']  # Returns value between -1 and 1
        except:
            return 0.0

# Enhanced Database Manager with Telegram community support
class EnhancedDatabaseManager:
    def __init__(self, db_path: str = "enhanced_fundraising_alerts.db"):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """Initialize database with enhanced tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Original tables
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                unique_id TEXT UNIQUE,
                project_name TEXT,
                stage TEXT,
                amount TEXT,
                investors TEXT,
                description TEXT,
                source_url TEXT,
                timestamp TEXT,
                followers_count INTEGER,
                community_size TEXT,
                project_age TEXT,
                social_metrics TEXT,
                sent BOOLEAN DEFAULT FALSE
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS subscribers (
                chat_id INTEGER PRIMARY KEY,
                subscribed_at TEXT,
                stages TEXT DEFAULT '[]',
                funding_amounts TEXT DEFAULT '[]',
                include_startups BOOLEAN DEFAULT TRUE,
                include_small_community BOOLEAN DEFAULT TRUE,
                include_newly_launched BOOLEAN DEFAULT TRUE,
                min_followers INTEGER DEFAULT 0,
                max_followers INTEGER DEFAULT 100000,
                telegram_communities BOOLEAN DEFAULT TRUE,
                community_size_filters TEXT DEFAULT '[]'
            )
        """)
        
        # New table for Telegram communities
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS telegram_communities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                unique_id TEXT UNIQUE,
                title TEXT,
                username TEXT,
                member_count INTEGER,
                description TEXT,
                admin_count INTEGER,
                creation_date TEXT,
                invite_link TEXT,
                legitimacy_score REAL,
                risk_level TEXT,
                scam_indicators TEXT,
                positive_indicators TEXT,
                tokenomics_analysis TEXT,
                roadmap_quality TEXT,
                team_analysis TEXT,
                sentiment_score REAL,
                discovery_timestamp TEXT,
                sent BOOLEAN DEFAULT FALSE
            )
        """)
        
        conn.commit()
        conn.close()
    
    def add_community_alert(self, alert: CommunityAlert) -> bool:
        """Add new community alert"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO telegram_communities (
                    unique_id, title, username, member_count, description,
                    admin_count, creation_date, invite_link, legitimacy_score,
                    risk_level, scam_indicators, positive_indicators,
                    tokenomics_analysis, roadmap_quality, team_analysis,
                    sentiment_score, discovery_timestamp
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                alert.unique_id,
                alert.community_info.title,
                alert.community_info.username,
                alert.community_info.member_count,
                alert.community_info.description,
                alert.community_info.admin_count,
                alert.community_info.creation_date.isoformat() if alert.community_info.creation_date else None,
                alert.community_info.invite_link,
                alert.project_analysis.legitimacy_score,
                alert.project_analysis.risk_level.value,
                json.dumps(alert.project_analysis.scam_indicators),
                json.dumps(alert.project_analysis.positive_indicators),
                alert.project_analysis.tokenomics_analysis,
                alert.project_analysis.roadmap_quality,
                alert.project_analysis.team_analysis,
                alert.project_analysis.sentiment_score,
                alert.discovery_timestamp.isoformat()
            ))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()
    
    def get_unsent_community_alerts(self) -> List[CommunityAlert]:
        """Get unsent community alerts"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM telegram_communities WHERE sent = FALSE")
        rows = cursor.fetchall()
        conn.close()
        
        alerts = []
        for row in rows:
            # Reconstruct objects from database row
            community_info = TelegramCommunityInfo(
                title=row[2],
                username=row[3],
                member_count=row[4],
                description=row[5],
                recent_messages=[],  # Not stored in DB for space
                admin_count=row[6],
                creation_date=datetime.fromisoformat(row[7]) if row[7] else None,
                invite_link=row[8],
                category="crypto",
                verified=False,
                restricted=False
            )
            
            project_analysis = ProjectAnalysis(
                legitimacy_score=row[9],
                scam_indicators=json.loads(row[11]),
                positive_indicators=json.loads(row[12]),
                risk_level=ScamRisk(row[10]),
                tokenomics_analysis=row[13],
                roadmap_quality=row[14],
                team_analysis=row[15],
                sentiment_score=row[16]
            )
            
            # Determine size category
            member_count = row[4]
            if 1 <= member_count <= 30:
                size_category = CommunitySize.MICRO
            elif 31 <= member_count <= 50:
                size_category = CommunitySize.SMALL
            elif 51 <= member_count <= 100:
                size_category = CommunitySize.MEDIUM_SMALL
            elif 101 <= member_count <= 200:
                size_category = CommunitySize.MEDIUM
            else:
                size_category = CommunitySize.GROWING
            
            alert = CommunityAlert(
                community_info=community_info,
                project_analysis=project_analysis,
                discovery_timestamp=datetime.fromisoformat(row[17]),
                unique_id=row[1],
                size_category=size_category
            )
            alerts.append(alert)
        
        return alerts
    
    def mark_community_alert_sent(self, unique_id: str):
        """Mark community alert as sent"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("UPDATE telegram_communities SET sent = TRUE WHERE unique_id = ?", (unique_id,))
        conn.commit()
        conn.close()

# Enhanced Telegram Bot with community scouting
class EnhancedTelegramBot:
    def __init__(self, token: str, db_manager: EnhancedDatabaseManager, 
                 monitor: 'Web3FundraisingMonitor', telegram_scout: Optional[TelegramScout] = None):
        self.token = token
        self.db = db_manager
        self.monitor = monitor
        self.telegram_scout = telegram_scout
        self.project_analyzer = ProjectAnalyzer(os.getenv('OPENAI_API_KEY'))
        self.bot = Bot(token)
        self.application = Application.builder().token(token).build()
        
        # Add research command handler
        self.application.add_handler(CommandHandler("research", self.research_project_command))
        self.project_researcher = ProjectResearcher(os.getenv('OPENAI_API_KEY'))
    
    async def research_project_command(self, update, context: ContextTypes.DEFAULT_TYPE):
        """Handle project research command"""
        if not context.args:
            await update.message.reply_text(
                "📊 **Project Research Command**\n\n"
                "Usage: `/research [project_name]`\n\n"
                "Example: `/research chainlink`\n"
                "This will provide comprehensive analysis including job opportunities and pitch guidance.",
                parse_mode='Markdown'
            )
            return
        
        project_name = ' '.join(context.args)
        
        # Send initial message
        research_msg = await update.message.reply_text(
            f"🔍 **Researching {project_name}...**\n\n"
            "This comprehensive analysis will take 30-60 seconds. Please wait...\n\n"
            "📊 Gathering data from multiple sources\n"
            "🤖 Running AI analysis\n"
            "💼 Identifying job opportunities\n"
            "📝 Preparing pitch strategies"
        )
        
        try:
            # Conduct comprehensive research
            analysis = await self.project_researcher.research_project_comprehensive(project_name)
            
            # Send detailed research results
            await self.send_comprehensive_research_results(update.effective_chat.id, analysis, research_msg.message_id)
            
        except Exception as e:
            logger.error(f"Error in project research: {e}")
            await self.bot.edit_message_text(
                chat_id=update.effective_chat.id,
                message_id=research_msg.message_id,
                text=f"❌ **Research Error**\n\nFailed to research {project_name}: {str(e)}\n\n"
                     f"Please try again or contact support."
            )
    
    async def send_comprehensive_research_results(self, chat_id: int, analysis: ComprehensiveProjectAnalysis, original_msg_id: int):
        """Send comprehensive research results in multiple messages"""
        
        # Message 1: Project Overview & Legitimacy
        overview_msg = self.format_project_overview(analysis)
        await self.bot.edit_message_text(
            chat_id=chat_id,
            message_id=original_msg_id,
            text=overview_msg,
            parse_mode='Markdown',
            disable_web_page_preview=True
        )
        
        # Message 2: Detailed Analysis
        analysis_msg = self.format_detailed_analysis(analysis)
        await self.bot.send_message(
            chat_id=chat_id,
            text=analysis_msg,
            parse_mode='Markdown',
            disable_web_page_preview=True
        )
        
        # Message 3: Job Opportunities & Pitch Strategies
        jobs_msg = self.format_job_opportunities(analysis)
        await self.bot.send_message(
            chat_id=chat_id,
            text=jobs_msg,
            parse_mode='Markdown',
            disable_web_page_preview=True
        )
        
        # Message 4: Action Plan & Next Steps
        action_msg = self.format_action_plan(analysis)
        await self.bot.send_message(
            chat_id=chat_id,
            text=action_msg,
            parse_mode='Markdown',
            disable_web_page_preview=True
        )
    
    def format_project_overview(self, analysis: ComprehensiveProjectAnalysis) -> str:
        """Format project overview message"""
        risk_emoji = {
            ScamRisk.LOW: "✅",
            ScamRisk.MEDIUM: "⚠️",
            ScamRisk.HIGH: "🔸",
            ScamRisk.CRITICAL: "🚨"
        }
        
        legitimacy = analysis.legitimacy_analysis
        risk_icon = risk_emoji.get(legitimacy.risk_level, "❓")
        
        # Warning text for high-risk projects
        warning_text = ""
        if legitimacy.risk_level in [ScamRisk.HIGH, ScamRisk.CRITICAL]:
            warning_text = f"\n🚨 **WARNING:** {', '.join(legitimacy.scam_indicators[:2])}\n"
        
        return f"""
📊 **COMPREHENSIVE PROJECT RESEARCH**

**{analysis.project_name.upper()}**
🌐 **Overall Maturity:** {analysis.project_needs.overall_maturity.title()}
{risk_icon} **Legitimacy Score:** {legitimacy.legitimacy_score:.1f}/100
🎯 **Risk Level:** {legitimacy.risk_level.value.upper()}

{warning_text}**📋 PROJECT DESCRIPTION:**
{analysis.project_description[:400]}{'...' if len(analysis.project_description) > 400 else ''}

**💪 STRENGTHS:**
{chr(10).join([f'✅ {strength.replace("_", " ").title()}' for strength in analysis.project_needs.strengths[:4]])}

**🔧 NEEDS IMPROVEMENT:**
{chr(10).join([f'❌ {area.replace("_", " ").title()}' for area in analysis.project_needs.improvement_areas[:4]])}

📅 **Research Date:** {analysis.research_timestamp.strftime('%Y-%m-%d %H:%M UTC')}
📚 **Sources:** {', '.join(analysis.sources_analyzed)}
        """
    
    def format_detailed_analysis(self, analysis: ComprehensiveProjectAnalysis) -> str:
        """Format detailed analysis message"""
        social = analysis.social_presence
        technical = analysis.technical_analysis
        team = analysis.team_analysis
        community = analysis.community_health
        tokenomics = analysis.tokenomics_deep_dive
        
        return f"""
🔍 **DETAILED ANALYSIS BREAKDOWN**

**📱 SOCIAL MEDIA PRESENCE** ({social['overall_score']}/100)
• Missing Platforms: {', '.join(social['missing_platforms']) if social['missing_platforms'] else 'None'}
• Twitter: {'✅' if social['twitter']['present'] else '❌'} ({social['twitter']['followers']:,} followers)
• Telegram: {'✅' if social['telegram']['present'] else '❌'} ({social['telegram']['members']:,} members)
• Discord: {'✅' if social['discord']['present'] else '❌'}

**🔧 TECHNICAL FOUNDATION** ({technical['technical_score']}/100)
• GitHub: {'✅' if technical['github']['present'] else '❌'}
• Whitepaper: {'✅' if technical['whitepaper']['present'] else '❌'}
• Smart Contracts: {'✅ Deployed' if technical['smart_contracts']['deployed'] else '❌ Not Found'}
• Security Audit: {'✅' if technical['smart_contracts']['audited'] else '❌'}

**👥 TEAM TRANSPARENCY** ({team['team_score']}/100)
• Transparency Level: {team['transparency'].title()}
• LinkedIn Profiles: {team['linkedin_profiles']}
• Public Backgrounds: {team['public_backgrounds']}

**💰 TOKENOMICS ANALYSIS** ({tokenomics['tokenomics_score']}/100)
• Burn Mechanism: {'✅' if tokenomics['burn_mechanism'] else '❌'}
• Staking: {'✅' if tokenomics['staking'] else '❌'}
• Governance: {'✅' if tokenomics['governance'] else '❌'}
• Red Flags: {', '.join(tokenomics['red_flags']) if tokenomics['red_flags'] else 'None identified'}

**👥 COMMUNITY HEALTH** ({community['community_score']}/100)
• Size: {community['size']}
• Engagement: {community['engagement_rate']}
• Sentiment: {community['community_sentiment'].title()}
        """
    
    def format_job_opportunities(self, analysis: ComprehensiveProjectAnalysis) -> str:
        """Format job opportunities message"""
        jobs = analysis.project_needs.job_opportunities
        
        if not jobs:
            return """
💼 **JOB OPPORTUNITIES & PITCH STRATEGIES**

🎯 **No specific job opportunities identified.**

This project appears to be well-staffed or mature. However, you can still reach out with:
• General consultation offers
• Specialized expertise in your field
• Partnership proposals
• Community contribution ideas
            """
        
        job_messages = []
        urgency_emoji = {"high": "🔥", "medium": "⚡", "low": "💡"}
        
        for i, job in enumerate(jobs[:4]):  # Show top 4 opportunities
            urgency_icon = urgency_emoji.get(job.urgency, "💼")
            job_msg = f"""
**{urgency_icon} {job.category.value.replace('_', ' ').upper()} - {job.urgency.upper()} PRIORITY**

📋 **Role:** {job.description}
💰 **Budget:** {job.estimated_budget}
⏰ **Commitment:** {job.time_commitment}

**Requirements:**
{chr(10).join([f'• {req}' for req in job.requirements])}

**🎯 HOW TO PITCH:**
{job.pitch_strategy}
            """
            job_messages.append(job_msg)
        
        return f"""
💼 **JOB OPPORTUNITIES & PITCH STRATEGIES**

Found **{len(jobs)} opportunities** for this project:

{''.join(job_messages)}

**📧 GENERAL OUTREACH TIPS:**
• Research recent project updates before reaching out
• Start with value - show what you can deliver
• Keep initial message concise (under 200 words)
• Follow up professionally if no response in 1 week
        """
    
    def format_action_plan(self, analysis: ComprehensiveProjectAnalysis) -> str:
        """Format action plan and next steps"""
        maturity = analysis.project_needs.overall_maturity
        
        if maturity == "early":
            stage_advice = """
**🌱 EARLY STAGE PROJECT**
• High potential but also high risk
• Focus on foundational roles (community, development)
• Consider equity/token compensation
• Be prepared for rapid changes
            """
        elif maturity == "developing":
            stage_advice = """
**📈 DEVELOPING PROJECT**
• Good balance of opportunity and stability
• Clear growth trajectory
• Professional compensation likely available
• Focus on scaling and optimization roles
            """
        else:
            stage_advice = """
**🏢 MATURE PROJECT**
• Lower risk, potentially lower growth
• Specialized roles and consulting opportunities
• Competitive compensation
• Focus on innovation and expansion roles
            """
        
        priority_actions = []
        for job in analysis.project_needs.job_opportunities[:3]:
            if job.urgency == "high":
                priority_actions.append(f"🔥 **{job.category.value.replace('_', ' ').title()}** - Act within 48 hours")
        
        return f"""
🎯 **ACTION PLAN & NEXT STEPS**

{stage_advice}

**⚡ PRIORITY ACTIONS:**
{chr(10).join(priority_actions) if priority_actions else '• Research project updates and recent news'}
• Join their community channels to understand culture
• Prepare portfolio/examples relevant to their needs
• Draft personalized outreach messages

**🔍 ADDITIONAL RESEARCH RECOMMENDED:**
• Recent partnership announcements
• Latest roadmap updates  
• Community sentiment analysis
• Competitor landscape
• Token price trends (if applicable)

**📞 NEXT STEPS:**
1. **Week 1:** Join communities, observe, contribute value
2. **Week 2:** Reach out with specific proposals
3. **Week 3:** Follow up and refine approach
4. **Week 4:** Consider alternative angles if needed

**⏰ Time-Sensitive Opportunities:** {len([j for j in analysis.project_needs.job_opportunities if j.urgency == 'high'])}

Use `/research [another_project]` to analyze more opportunities!
        """
    
    async def start_command(self, update, context: ContextTypes.DEFAULT_TYPE):
        """Enhanced start command with research feature"""
        welcome_msg = """
🚀 **Welcome to Enhanced Web3 Fundraising & Community Monitor!**

This advanced bot now includes **comprehensive project research** with job opportunity analysis!

📊 **What I Can Do:**

**🔍 PROJECT RESEARCH** 🆕
• Deep dive analysis of any web3 project
• Job opportunity identification
• Personalized pitch strategies
• Team & technical assessment
• Risk evaluation with scam detection

**📱 MONITORING & ALERTS**
• Funding rounds (Pre-seed to Series C)
• Telegram communities (1-200 members)
• Twitter & news sources
• AI-powered legitimacy scoring

**💼 JOB OPPORTUNITIES** 🆕
• Community Management
• Social Media & Marketing  
• Graphics Design & Branding
• Business Development
• Technical Writing
• And much more!

**📋 COMMANDS:**
/research [project_name] - 🆕 **Comprehensive project analysis**
/subscribe - Start receiving alerts
/preferences - Customize notifications  
/scout_communities - Manual community scan
/status - Check your settings

**💡 EXAMPLE:**
`/research chainlink` - Get detailed analysis with job opportunities

Get started with /subscribe or try /research with any project name!
        """
        await update.message.reply_text(welcome_msg, parse_mode='Markdown')
    
    async def scout_communities_command(self, update, context: ContextTypes.DEFAULT_TYPE):
        """Manual community scouting command"""
        if not self.telegram_scout:
            await update.message.reply_text(
                "❌ Telegram scouting not configured. Please set up API credentials."
            )
            return
        
        await update.message.reply_text(
            "🔍 **Starting manual community scan...**\n\n"
            "This may take a few minutes. I'll search for small web3 communities and analyze them for legitimacy."
        )
        
        try:
            # Scout communities with all size filters
            size_filters = [CommunitySize.MICRO, CommunitySize.SMALL, 
                          CommunitySize.MEDIUM_SMALL, CommunitySize.MEDIUM]
            
            communities = await self.telegram_scout.search_crypto_communities(size_filters)
            
            if not communities:
                await update.message.reply_text("🔍 No new communities found in this scan.")
                return
            
            # Analyze each community
            new_alerts = 0
            for community in communities:
                try:
                    # Analyze the project
                    analysis = await self.project_analyzer.analyze_project(community)
                    
                    # Create alert
                    unique_content = f"{community.title}{community.username}"
                    unique_id = hashlib.md5(unique_content.encode()).hexdigest()
                    
                    # Determine size category
                    if 1 <= community.member_count <= 30:
                        size_category = CommunitySize.MICRO
                    elif 31 <= community.member_count <= 50:
                        size_category = CommunitySize.SMALL
                    elif 51 <= community.member_count <= 100:
                        size_category = CommunitySize.MEDIUM_SMALL
                    elif 101 <= community.member_count <= 200:
                        size_category = CommunitySize.MEDIUM
                    else:
                        size_category = CommunitySize.GROWING
                    
                    alert = CommunityAlert(
                        community_info=community,
                        project_analysis=analysis,
                        discovery_timestamp=datetime.now(),
                        unique_id=unique_id,
                        size_category=size_category
                    )
                    
                    if self.db.add_community_alert(alert):
                        new_alerts += 1
                        
                except Exception as e:
                    logger.error(f"Error analyzing community {community.title}: {e}")
                    continue
            
            # Send immediate results to the user
            await self.send_community_scan_results(update.effective_chat.id, new_alerts)
            
            # Broadcast to subscribers
            await self.broadcast_community_alerts()
            
        except Exception as e:
            logger.error(f"Error in manual community scan: {e}")
            await update.message.reply_text(f"❌ Error during community scan: {str(e)}")
    
    async def send_community_scan_results(self, chat_id: int, new_alerts: int):
        """Send scan results to user"""
        if new_alerts > 0:
            await self.bot.send_message(
                chat_id=chat_id,
                text=f"✅ **Scan Complete!**\n\nFound {new_alerts} new communities to analyze. "
                     f"Alerts are being processed and will be sent based on your preferences."
            )
        else:
            await self.bot.send_message(
                chat_id=chat_id,
                text="🔍 **Scan Complete!**\n\nNo new communities found that match the criteria."
            )
    
    async def preferences_command(self, update, context: ContextTypes.DEFAULT_TYPE):
        """Enhanced preferences with community options"""
        keyboard = [
            [InlineKeyboardButton("🎯 Project Stages", callback_data="pref_stages")],
            [InlineKeyboardButton("💰 Funding Amounts", callback_data="pref_amounts")],
            [InlineKeyboardButton("👥 Community Size", callback_data="pref_community")],
            [InlineKeyboardButton("📱 Telegram Communities", callback_data="pref_telegram_communities")],
            [InlineKeyboardButton("📊 Current Settings", callback_data="pref_status")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "⚙️ **Customize Your Notification Preferences**\n\n"
            "Choose what you want to configure:",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    async def handle_callback(self, update, context: ContextTypes.DEFAULT_TYPE):
        """Enhanced callback handler with community preferences"""
        query = update.callback_query
        await query.answer()
        
        chat_id = query.message.chat_id
        data = query.data
        
        if data == "pref_telegram_communities":
            await self.show_telegram_community_preferences(query, chat_id)
        elif data.startswith("toggle_tg_size_"):
            await self.toggle_telegram_size_preference(query, chat_id, data)
        elif data == "toggle_tg_communities":
            await self.toggle_telegram_communities(query, chat_id)
        else:
            # Handle existing callbacks from previous implementation
            await self.handle_existing_callbacks(query, chat_id, data)
    
    async def show_telegram_community_preferences(self, query, chat_id: int):
        """Show Telegram community preferences"""
        prefs = self.db.get_user_preferences(chat_id)
        if not prefs:
            await query.edit_message_text("❌ Please subscribe first using /subscribe")
            return
        
        # Get current community size filters
        community_filters = getattr(prefs, 'community_size_filters', [])
        telegram_enabled = getattr(prefs, 'telegram_communities', True)
        
        keyboard = []
        
        # Toggle for telegram communities
        tg_status = "✅" if telegram_enabled else "❌"
        keyboard.append([InlineKeyboardButton(
            f"{tg_status} Enable Telegram Scouting",
            callback_data="toggle_tg_communities"
        )])
        
        if telegram_enabled:
            # Community size options
            size_options = [
                (CommunitySize.MICRO, "👶 Micro (1-30 members)"),
                (CommunitySize.SMALL, "🤏 Small (31-50 members)"),
                (CommunitySize.MEDIUM_SMALL, "📈 Medium Small (51-100 members)"),
                (CommunitySize.MEDIUM, "🎯 Medium (101-200 members)"),
                (CommunitySize.GROWING, "🌱 Growing (201-500 members)"),
            ]
            
            for size, label in size_options:
                status = "✅" if size.value in community_filters else "❌"
                keyboard.append([InlineKeyboardButton(
                    f"{status} {label}",
                    callback_data=f"toggle_tg_size_{size.value}"
                )])
        
        keyboard.append([InlineKeyboardButton("⬅️ Back", callback_data="back_to_main")])
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            "📱 **Telegram Community Scouting**\n\n"
            "Configure which Telegram communities to monitor:\n\n"
            "🤖 **Features:**\n"
            "• AI-powered legitimacy analysis\n"
            "• Scam detection with risk warnings\n"
            "• Project quality assessment\n"
            "• Team transparency analysis\n\n"
            "Select community sizes to monitor:",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    async def send_community_alert(self, alert: CommunityAlert, chat_id: int):
        """Send community alert with detailed analysis"""
        risk_emoji = {
            ScamRisk.LOW: "✅",
            ScamRisk.MEDIUM: "⚠️", 
            ScamRisk.HIGH: "🔸",
            ScamRisk.CRITICAL: "🚨"
        }
        
        risk_color = risk_emoji.get(alert.project_analysis.risk_level, "❓")
        
        # Format scam warnings
        warning_text = ""
        if alert.project_analysis.risk_level in [ScamRisk.HIGH, ScamRisk.CRITICAL]:
            scam_indicators = alert.project_analysis.scam_indicators[:3]  # Show top 3
            warning_text = f"\n🚨 **WARNING SIGNS:** {', '.join(scam_indicators)}\n"
        
        # Format positive indicators
        positive_text = ""
        if alert.project_analysis.positive_indicators:
            positive_indicators = alert.project_analysis.positive_indicators[:3]
            positive_text = f"\n✅ **POSITIVE SIGNS:** {', '.join(positive_indicators)}\n"
        
        # Sentiment emoji
        sentiment = alert.project_analysis.sentiment_score
        sentiment_emoji = "😊" if sentiment > 0.1 else "😐" if sentiment > -0.1 else "😟"
        
        message = f"""
📱 **NEW TELEGRAM COMMUNITY FOUND**

**{alert.community_info.title}**
👥 **Members:** {alert.community_info.member_count} ({alert.size_category.value})
🔗 **Link:** {alert.community_info.invite_link or 'Private'}

{risk_color} **Legitimacy Score:** {alert.project_analysis.legitimacy_score:.1f}/100
🎯 **Risk Level:** {alert.project_analysis.risk_level.value.upper()}
{sentiment_emoji} **Sentiment:** {sentiment:.2f}

**📋 PROJECT OVERVIEW:**
{alert.community_info.description[:300]}{'...' if len(alert.community_info.description) > 300 else ''}

{warning_text}{positive_text}

**🔍 DETAILED ANALYSIS:**
💰 **Tokenomics:** {alert.project_analysis.tokenomics_analysis or 'Not analyzed'}
🗺️ **Roadmap:** {alert.project_analysis.roadmap_quality or 'No roadmap info'}
👥 **Team:** {alert.project_analysis.team_analysis or 'Team info limited'}

**👮‍♂️ Admins:** {alert.community_info.admin_count}
📅 **Discovered:** {alert.discovery_timestamp.strftime('%Y-%m-%d %H:%M UTC')}

{"⚠️ **PROCEED WITH EXTREME CAUTION** ⚠️" if alert.project_analysis.risk_level == ScamRisk.CRITICAL else ""}
        """
        
        try:
            await self.bot.send_message(
                chat_id=chat_id,
                text=message,
                parse_mode='Markdown',
                disable_web_page_preview=True
            )
        except Exception as e:
            logger.error(f"Failed to send community alert to {chat_id}: {e}")
    
    def should_send_community_to_user(self, alert: CommunityAlert, prefs) -> bool:
        """Check if community alert matches user preferences"""
        # Check if telegram communities are enabled
        telegram_enabled = getattr(prefs, 'telegram_communities', True)
        if not telegram_enabled:
            return False
        
        # Check community size filters
        community_filters = getattr(prefs, 'community_size_filters', [])
        if community_filters and alert.size_category.value not in community_filters:
            return False
        
        # Don't send critical risk projects unless user specifically opts in
        if alert.project_analysis.risk_level == ScamRisk.CRITICAL:
            # Could add a user preference for this
            return False
        
        return True
    
    async def broadcast_community_alerts(self):
        """Broadcast community alerts to subscribers"""
        alerts = self.db.get_unsent_community_alerts()
        subscribers = self.db.get_subscribers()
        
        for alert in alerts:
            sent_count = 0
            for chat_id in subscribers:
                prefs = self.db.get_user_preferences(chat_id)
                if prefs and self.should_send_community_to_user(alert, prefs):
                    await self.send_community_alert(alert, chat_id)
                    sent_count += 1
                    await asyncio.sleep(0.2)  # Rate limiting
            
            # Mark as sent
            self.db.mark_community_alert_sent(alert.unique_id)
            if sent_count > 0:
                logger.info(f"Sent community alert for {alert.community_info.title} to {sent_count} subscribers")
    
    async def community_monitoring_job(self):
        """Background job for community monitoring"""
        if not self.telegram_scout:
            logger.info("Telegram scout not configured - skipping community monitoring")
            return
        
        while True:
            try:
                logger.info("Starting Telegram community monitoring cycle...")
                
                # Define size filters for automatic monitoring
                size_filters = [CommunitySize.MICRO, CommunitySize.SMALL, 
                              CommunitySize.MEDIUM_SMALL, CommunitySize.MEDIUM]
                
                communities = await self.telegram_scout.search_crypto_communities(size_filters)
                
                new_alerts = 0
                for community in communities:
                    try:
                        # Analyze the project
                        analysis = await self.project_analyzer.analyze_project(community)
                        
                        # Create alert
                        unique_content = f"{community.title}{community.username}"
                        unique_id = hashlib.md5(unique_content.encode()).hexdigest()
                        
                        # Determine size category
                        if 1 <= community.member_count <= 30:
                            size_category = CommunitySize.MICRO
                        elif 31 <= community.member_count <= 50:
                            size_category = CommunitySize.SMALL
                        elif 51 <= community.member_count <= 100:
                            size_category = CommunitySize.MEDIUM_SMALL
                        elif 101 <= community.member_count <= 200:
                            size_category = CommunitySize.MEDIUM
                        else:
                            size_category = CommunitySize.GROWING
                        
                        alert = CommunityAlert(
                            community_info=community,
                            project_analysis=analysis,
                            discovery_timestamp=datetime.now(),
                            unique_id=unique_id,
                            size_category=size_category
                        )
                        
                        if self.db.add_community_alert(alert):
                            new_alerts += 1
                            
                    except Exception as e:
                        logger.error(f"Error analyzing community {community.title}: {e}")
                        continue
                
                if new_alerts > 0:
                    logger.info(f"Found {new_alerts} new Telegram communities")
                    await self.broadcast_community_alerts()
                else:
                    logger.info("No new Telegram communities found")
                    
            except Exception as e:
                logger.error(f"Error in community monitoring job: {e}")
            
            # Wait 2 hours before next community scan (less frequent than other sources)
            await asyncio.sleep(7200)
    
    async def enhanced_monitoring_job(self):
        """Enhanced monitoring job combining all sources"""
        # Start both monitoring jobs
        web_monitor_task = asyncio.create_task(self.web_monitoring_job())
        community_monitor_task = asyncio.create_task(self.community_monitoring_job())
        
        try:
            await asyncio.gather(web_monitor_task, community_monitor_task)
        except Exception as e:
            logger.error(f"Error in enhanced monitoring: {e}")
    
    async def web_monitoring_job(self):
        """Original web monitoring job"""
        while True:
            try:
                logger.info("Starting web monitoring cycle...")
                alerts = await self.monitor.monitor_sources()
                
                new_alerts = 0
                for alert in alerts:
                    if self.db.add_alert(alert):
                        new_alerts += 1
                
                if new_alerts > 0:
                    logger.info(f"Found {new_alerts} new funding alerts")
                    await self.broadcast_alerts()
                else:
                    logger.info("No new funding alerts found")
                
            except Exception as e:
                logger.error(f"Error in web monitoring job: {e}")
            
            # Wait 30 minutes
            await asyncio.sleep(1800)
    
    async def start_enhanced_bot(self):
        """Start the enhanced bot with all monitoring capabilities"""
        await self.application.initialize()
        await self.application.start()
        
        # Start all monitoring jobs
        web_monitor_task = asyncio.create_task(self.web_monitoring_job())
        community_monitor_task = asyncio.create_task(self.community_monitoring_job())
        
        # Start polling
        polling_task = asyncio.create_task(self.application.updater.start_polling())
        
        # Wait for all tasks
        try:
            await asyncio.gather(web_monitor_task, community_monitor_task, polling_task)
        except KeyboardInterrupt:
            logger.info("Stopping enhanced bot...")
        finally:
            await self.monitor.close_session()
            if self.telegram_scout:
                await self.telegram_scout.close()
            await self.project_researcher.close_session()
            await self.application.stop()

def main():
    """Enhanced main function with Telegram scouting"""
    # Get tokens from environment variables
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    twitter_bearer_token = os.getenv('TWITTER_BEARER_TOKEN')
    
    # Telegram API credentials for scouting
    telegram_api_id = os.getenv('TELEGRAM_API_ID')
    telegram_api_hash = os.getenv('TELEGRAM_API_HASH')
    telegram_phone = os.getenv('TELEGRAM_PHONE_NUMBER')
    
    if not bot_token:
        logger.error("Please set TELEGRAM_BOT_TOKEN environment variable")
        return
    
    # Initialize components
    db_manager = EnhancedDatabaseManager()
    monitor = Web3FundraisingMonitor(twitter_bearer_token)
    
    # Initialize Telegram scout if credentials available
    telegram_scout = None
    if all([telegram_api_id, telegram_api_hash, telegram_phone]):
        try:
            telegram_scout = TelegramScout(
                api_id=int(telegram_api_id),
                api_hash=telegram_api_hash,
                phone_number=telegram_phone
            )
            logger.info("Telegram scouting enabled")
        except Exception as e:
            logger.warning(f"Could not initialize Telegram scout: {e}")
    else:
        logger.warning("Telegram scouting disabled - missing API credentials")
    
    bot = EnhancedTelegramBot(bot_token, db_manager, monitor, telegram_scout)
    
    # Run the enhanced bot
    asyncio.run(bot.start_enhanced_bot())

if __name__ == "__main__":
    main()
